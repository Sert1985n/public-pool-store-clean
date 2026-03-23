
const UI = window.PUBLIC_POOL_UI || {};
const fmtNum = n => (n === null || n === undefined || Number.isNaN(Number(n))) ? '—' : Number(n).toLocaleString('en-US');
const fmtPct = n => (n === null || n === undefined || Number.isNaN(Number(n))) ? '—' : `${Number(n).toFixed(2)}%`;
const fmtHashrate = n => {
  const v = Number(n);
  if(!Number.isFinite(v) || v <= 0) return '—';
  const units = ['H/s','KH/s','MH/s','GH/s','TH/s','PH/s','EH/s'];
  let i=0, val=v;
  while(val >= 1000 && i < units.length-1){ val /= 1000; i++; }
  return `${val.toFixed(val >= 100 ? 0 : val >= 10 ? 1 : 2)} ${units[i]}`;
};
const fmtPrice = n => {
  const v = Number(n);
  if(!Number.isFinite(v) || v <= 0) return '—';
  return `$${v.toLocaleString('en-US', { maximumFractionDigits: 8 })}`;
};
function api(path){ return `${UI.apiBase}${path}`; }
async function fetchJson(url){ const r = await fetch(url, {cache:'no-store'}); if(!r.ok) throw new Error(`HTTP ${r.status}`); return await r.json(); }
async function fetchPools(){ const data = await fetchJson(api('/pools')); return data.pools || []; }
function poolStat(pool, keys){
  for(const k of keys){
    const parts = k.split('.');
    let v = pool;
    for(const p of parts){ v = v?.[p]; }
    if(v !== undefined && v !== null) return v;
  }
  return null;
}
function homeLinkFor(id){
  const port = UI.ports[id];
  return `${location.protocol}//${location.hostname}:${port}`;
}
function setMeta(title, footerLabel){
  document.title = title;
  const footer = document.getElementById('footer-text');
  if(footer) footer.textContent = footerLabel || UI.footer;
}
function coinIcon(id){
  const coin = UI.coins.find(c => c.id === id);
  return `icons/${coin?.icon || 'generic.png'}`;
}
async function renderHome(){
  setMeta(`${UI.brandName} — SOLO Mining Pool`, UI.footer);
  const app = document.getElementById('app');
  app.innerHTML = `<section class="hero"><h1>${UI.brandName}</h1><p>SOLO mining pool frontend with live backend data from Miningcore API.</p></section><section class="metrics" id="global-metrics"></section><section class="coins-grid" id="coins-grid"></section>`;
  let pools = [];
  try { pools = await fetchPools(); } catch(err){
    app.innerHTML = `<div class="notice">Не удалось получить данные из API: ${err.message}. Убедись, что Miningcore доступен на порту 4000 текущего сервера.</div>`;
    return;
  }
  const wanted = UI.coins.map(c => c.id);
  const visible = wanted.map(id => pools.find(p => p.id === id)).filter(Boolean);
  const miners = visible.reduce((s,p) => s + Number(poolStat(p,['poolStats.connectedMiners','connectedMiners','minersTotal']) || 0), 0);
  const hashrate = visible.reduce((s,p) => s + Number(poolStat(p,['poolStats.poolHashrate','poolHashrate','hashrate']) || 0), 0);
  const difficulty = visible.reduce((s,p) => s + Number(poolStat(p,['networkStats.networkDifficulty','networkDifficulty']) || 0), 0);
  const price = visible.reduce((s,p) => s + Number(poolStat(p,['price','priceUsd','coin.price']) || 0), 0);
  const global = [
    ['Coins', visible.length],
    ['Miners', miners],
    ['Pool Hashrate', fmtHashrate(hashrate)],
    ['Network Difficulty', fmtNum(difficulty)],
    ['Price Sum', fmtPrice(price)],
  ];
  document.getElementById('global-metrics').innerHTML = global.map(([label,val]) => `<div class="metric"><div class="label">${label}</div><div class="value">${typeof val === 'number' ? fmtNum(val) : val}</div></div>`).join('');
  const grid = document.getElementById('coins-grid');
  grid.innerHTML = wanted.map(id => {
    const pool = pools.find(p => p.id === id);
    const info = UI.coins.find(c => c.id === id);
    const miners = pool ? fmtNum(poolStat(pool,['poolStats.connectedMiners','connectedMiners','minersTotal'])) : '—';
    const rate = pool ? fmtHashrate(poolStat(pool,['poolStats.poolHashrate','poolHashrate','hashrate'])) : '—';
    const diff = pool ? fmtNum(poolStat(pool,['networkStats.networkDifficulty','networkDifficulty'])) : '—';
    const price = pool ? fmtPrice(poolStat(pool,['price','priceUsd','coin.price'])) : '—';
    return `<a class="coin-card" href="${homeLinkFor(id)}"><img src="${coinIcon(id)}" alt="${info.symbol}"><div><div class="symbol">${info.symbol}</div><div class="name">${info.title}</div><div class="row">Miners: ${miners}</div><div class="row">Hashrate: ${rate}</div><div class="row">Difficulty: ${diff}</div><div class="row">Price: ${price}</div></div></a>`;
  }).join('');
}
async function fetchPool(id){ const pools = await fetchPools(); return pools.find(p => p.id === id); }
function helpRows(pool, currentId){
  const portEntries = Object.entries(pool?.ports || {}).sort((a,b) => Number(a[0]) - Number(b[0]));
  const labels = ['Low-End Hardware','Mid-Range Hardware','High-End Hardware','NerdMiner'];
  return portEntries.map(([port,meta], idx) => ({
    label: labels[idx] || meta?.name || `Port ${port}`,
    endpoint: `stratum+tcp://${location.hostname}:${port}`,
    difficulty: meta?.difficulty ?? '—'
  }));
}
async function fetchTableJson(candidates){
  for(const c of candidates){
    try { return await fetchJson(api(c)); } catch(err) {}
  }
  return null;
}
function renderTable(rows, columns){
  if(!rows || !rows.length) return `<div class="notice">Данных пока нет или endpoint ещё не отвечает.</div>`;
  return `<div class="tablewrap"><table><thead><tr>${columns.map(c=>`<th>${c.label}</th>`).join('')}</tr></thead><tbody>${rows.map(r=>`<tr>${columns.map(c=>`<td>${c.render(r)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
}
async function renderCoin(id){
  const app = document.getElementById('app');
  const tab = (location.hash.split('/')[2] || 'home').toLowerCase();
  let pool;
  try { pool = await fetchPool(id); } catch(err){
    app.innerHTML = `<div class="notice">Не удалось получить пул ${id.toUpperCase()} из API: ${err.message}</div>`;
    return;
  }
  const info = UI.coins.find(c => c.id === id) || { title:id.toUpperCase(), symbol:id.toUpperCase() };
  setMeta(`${info.title} (${info.symbol}) — SOLO Mining Pool`, `${info.title} (${info.symbol}) © public-pool-btc.ru - 2026`);
  const homeHref = `${location.protocol}//${location.hostname}:8500`;
  const nav = ['home','blocks','miners','help','pools'].map(t => `<a class="tabbtn ${tab===t?'active':''}" href="#/${id}/${t}">${t[0].toUpperCase()+t.slice(1)}</a>`).join('');
  const summary = `
    <div class="grid2">
      <div class="panel"><div class="brand" style="font-size:24px"><img src="${coinIcon(id)}" alt="${info.symbol}" style="width:42px;height:42px"> <span>${info.title} (${info.symbol})</span></div><div class="subtitle">Pools always return to 8500. Help shows only RU stratum lines from live config.</div><div class="navtabs">${nav}</div><div id="tab-content"></div></div>
      <div class="panel"><div class="statsgrid">
        <div class="metric"><div class="label">Miners</div><div class="value">${fmtNum(poolStat(pool,['poolStats.connectedMiners','connectedMiners','minersTotal']))}</div></div>
        <div class="metric"><div class="label">Pool Hashrate</div><div class="value">${fmtHashrate(poolStat(pool,['poolStats.poolHashrate','poolHashrate','hashrate']))}</div></div>
        <div class="metric"><div class="label">Network Hashrate</div><div class="value">${fmtHashrate(poolStat(pool,['networkStats.networkHashrate','networkHashrate']))}</div></div>
        <div class="metric"><div class="label">Difficulty</div><div class="value">${fmtNum(poolStat(pool,['networkStats.networkDifficulty','networkDifficulty']))}</div></div>
        <div class="metric"><div class="label">Price</div><div class="value">${fmtPrice(poolStat(pool,['price','priceUsd','coin.price']))}</div></div>
        <div class="metric"><div class="label">Pool Effort</div><div class="value">${fmtPct(poolStat(pool,['poolEffort']))}</div></div>
      </div></div>
    </div>`;
  app.innerHTML = summary;
  const target = document.getElementById('tab-content');
  if(tab === 'pools'){
    target.innerHTML = `<div class="notice"><a href="${homeHref}">Вернуться на главную 8500</a></div>`;
    return;
  }
  if(tab === 'help'){
    const rows = helpRows(pool,id);
    target.innerHTML = `<div class="help-list">${rows.map(r => `<div class="help-item"><div><div><strong>${r.label}</strong></div><div class="small">${r.endpoint}</div></div><div><strong>Diff ${r.difficulty}</strong></div></div>`).join('')}</div>`;
    return;
  }
  if(tab === 'blocks'){
    const data = await fetchTableJson([`/pools/${id}/blocks?page=0&pageSize=100`,`/pools/${id}/blocks`]);
    const rows = data?.result || data?.blocks || data || [];
    target.innerHTML = renderTable(rows, [
      {label:'Height', render:r => r.blockHeight ?? r.height ?? '—'},
      {label:'Status', render:r => r.status ?? '—'},
      {label:'Effort', render:r => r.effort ?? '—'},
      {label:'Reward', render:r => r.reward ?? r.rewardAmount ?? '—'},
      {label:'Created', render:r => r.created ?? r.createdDate ?? r.time ?? '—'}
    ]);
    return;
  }
  if(tab === 'miners'){
    const data = await fetchTableJson([`/pools/${id}/miners?page=0&pageSize=100`,`/pools/${id}/miners`]);
    const rows = data?.result || data?.miners || data || [];
    target.innerHTML = renderTable(rows, [
      {label:'Miner', render:r => r.miner ?? r.address ?? r.worker ?? '—'},
      {label:'Hashrate', render:r => fmtHashrate(r.hashrate ?? r.currentHashrate ?? r.sharesPerSecond)},
      {label:'Shares', render:r => fmtNum(r.shares ?? r.validShares ?? r.pendingShares)},
      {label:'Last Share', render:r => r.lastShare ?? r.lastShareTime ?? '—'}
    ]);
    return;
  }
  target.innerHTML = `<div class="panel" style="padding:0;background:none;border:none"><div class="notice">Help и статистика строятся из live API текущего Miningcore. Для ${info.symbol} страница уже привязана к правильной навигации и текущему серверу.</div></div>`;
}
function route(){
  const hash = location.hash.replace(/^#\/?/,'');
  if(!hash){ renderHome(); return; }
  const [id] = hash.split('/');
  if(UI.coins.some(c => c.id === id)) renderCoin(id); else renderHome();
}
window.addEventListener('hashchange', route);
window.addEventListener('DOMContentLoaded', route);
