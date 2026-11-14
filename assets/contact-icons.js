/* Значки для связи в шапке: Telegram, Max, Email, LinkedIn, телефон. Только логотипы, без подписей. */
(function(){
  if(window.__aimIc)return;window.__aimIc=1;
  var d=document;
  var LI="https://www.linkedin.com/in/andreyafomin/";
  var L=[
    ["Telegram","https://t.me/AndreyAFomin","#229ED9",'<path fill="#fff" d="M9.4 15.6l-.3 3.9c.4 0 .6-.2.8-.4l1.9-1.8 3.9 2.9c.7.4 1.2.2 1.4-.7l2.6-12.2c.3-1.1-.4-1.6-1.1-1.3L4.3 12.1c-1.1.4-1.1 1-.2 1.3l3.9 1.2 9-5.7c.4-.3.8-.1.5.2z"/>'],
    ["Max","https://max.ru/u/f9LHodD0cOLLKaKK0Pz2ioVL4umNqnv5eljhNlv-D9DrnW10TnSXLnm2hx8","linear-gradient(135deg,#2AA7FF,#7A3CF0)",'<path fill="#fff" d="M12 4.5c-4.1 0-7.3 3.1-7.3 7.2 0 1.5.4 2.8 1.2 4-.1 1-.5 2.1-1.2 2.9 1.4 0 2.6-.5 3.5-1.2 1.1.6 2.3.9 3.8.9 4.1 0 7.3-3.1 7.3-7.2S16.100 4.500 12 4.500zm-3.300 8.700V9.200h1.100l1.600 2.400 1.600-2.400h1.100v4h-1.100v-2.300l-1.600 2.300-1.600-2.300v2.300z"/>'],
    ["Email","mailto:af@aiminterims.ru","#6B6B72",'<path fill="#fff" d="M5 6.500h14c.8 0 1.500.7 1.500 1.500v8c0 .8-.7 1.500-1.500 1.500H5c-.8 0-1.500-.7-1.500-1.500V8c0-.8.7-1.500 1.500-1.500zm0 1.800v.3l7 4.400 7-4.400v-.3zm14 2.500l-7 4.400-7-4.400V16h14z"/>'],
    ["LinkedIn",LI,"#0A66C2",'<path fill="#fff" d="M7.100 9.500H4.500V19h2.600zM5.800 5.500a1.500 1.500 0 100 3 1.500 1.500 0 000-3zM19.500 13.700c0-2.600-1.400-4.400-3.700-4.400-1.100 0-2 .6-2.400 1.300V9.500h-2.500V19h2.600v-5.200c0-1.100.6-1.800 1.500-1.800.9 0 1.400.6 1.400 1.800V19h2.600z"/>'],
    ["Позвонить","tel:+79119711519","#2EB872",'<path fill="#fff" d="M8.200 4.500l2 3.800-1.300 1.300c.9 1.800 2.300 3.200 4.100 4.100l1.300-1.300 3.800 2c.1 1.400-1 2.600-2.400 2.600C9.800 17 7 14.200 5.600 10.600 5.500 9.100 6.700 8 8.200 4.500z"/>']
  ];
  var css=".am-ic{display:flex;align-items:center;gap:10px;flex:0 0 auto}.am-ic a{display:flex;width:34px;height:34px;border-radius:50%;align-items:center;justify-content:center;transition:border-color .15s,background .15s}.am-ic a{background:rgba(244,242,238,.06)!important;border:1px solid rgba(244,242,238,.28);box-sizing:border-box}.am-ic a svg path{fill:#f4f2ee}.am-ic a:hover{border-color:#E8A33D;background:rgba(232,163,61,.12)!important}.am-ic a:hover svg path{fill:#E8A33D}.am-ic svg{width:20px;height:20px;display:block}header .nav ul a,header .nav>.btn{white-space:nowrap}@media(min-width:981px) and (max-width:1320px){header .nav{gap:12px}header .nav ul{gap:14px}header .nav ul a{font-size:14px}header .nav>.btn{padding:9px 14px;font-size:14px}.am-ic{gap:7px}.am-ic a{width:30px;height:30px}}@media(max-width:640px){.am-ic{gap:6px}.am-ic a{width:28px;height:28px}.am-ic svg{width:17px;height:17px}}@media(max-width:400px){.am-ic{gap:4px}.am-ic a{width:26px;height:26px}header.top img,header .nav>a>img{max-width:30vw!important}}";
  function init(){
    var hdr=d.querySelector("body > header, header");
    var bar=!hdr&&d.querySelector(".am-bar");var fx=!hdr&&(!bar||getComputedStyle(bar).display==="none");
    var st=d.createElement("style");st.textContent=css+".am-ic.fx{position:fixed;top:12px;right:max(16px,env(safe-area-inset-right,0px));z-index:40;padding:6px 10px;border-radius:999px;background:rgba(35,35,37,.92);box-shadow:0 2px 12px rgba(0,0,0,.25)}@media(max-width:980px){.am-ic.fx{display:none}}";d.head.appendChild(st);
    var host=hdr?(hdr.querySelector(".nav")||hdr):(bar||d.body);
    var w=d.createElement("div");w.className="am-ic";
    L.forEach(function(i){
      if(!i[1])return;
      var a=d.createElement("a");a.href=i[1];a.setAttribute("aria-label",i[0]);a.title=i[0];
      if(/^https/.test(i[1])){a.target="_blank";a.rel="noopener"}
      a.style.background=i[2];
      a.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true">'+i[3]+'</svg>';
      w.appendChild(a);
    });
    if(fx){w.className+=" fx";d.body.appendChild(w);return}
    var ref=host.querySelector(":scope > .btn, :scope > .chip, :scope > .am-btn");
    if(ref)host.insertBefore(w,ref);else host.appendChild(w);
  }
  setTimeout(init,0);
})();
