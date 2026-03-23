window.PUBLIC_POOL_UI = {
  brandName: 'public-pool-btc.ru',
  footer: '© public-pool-btc.ru - 2026',
  apiBase: `${location.protocol}//${location.hostname}:4000/api`,
  siteBase: `${location.protocol}//${location.hostname}`,
  ports: {
    home: 8500,
    btc: 8501,
    bch: 8502,
    bc2: 8503,
    btcs: 8504,
    lcc: 8505,
    wjk: 8506,
    rvn: 8507
  },
  coins: [
    { id: 'btc', title: 'Bitcoin', symbol: 'BTC', icon: 'btc.png' },
    { id: 'bch', title: 'Bitcoin Cash', symbol: 'BCH', icon: 'bch.png' },
    { id: 'bc2', title: 'Bitcoin II', symbol: 'BC2', icon: 'bc2.png' },
    { id: 'btcs', title: 'Bitcoin Silver', symbol: 'BTCS', icon: 'btcs.png' },
    { id: 'lcc', title: 'Litecoin Cash', symbol: 'LCC', icon: 'lcc.png' },
    { id: 'wjk', title: 'WojakCoin', symbol: 'WJK', icon: 'wjk.png' },
    { id: 'rvn', title: 'Ravencoin', symbol: 'RVN', icon: 'rvn.png' }
  ]
};
