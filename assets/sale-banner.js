/* Баннер распродажи АИМ 11.11-13.11: красные ценники и мигающая ссылка в меню. Скрывается сам после 13.11 23:59 МСК. */
(function(){
  if(Date.now()>=Date.parse("2026-11-14T00:00:00+03:00"))return;
  var d=document,onSale=/^\/sale\/?$/.test(location.pathname),href=onSale?"#offers":"/sale/";
  var css=
  ".sb{display:block;position:relative;z-index:30;text-decoration:none;color:#fff;overflow:hidden;background:radial-gradient(600px 160px at 50% 100%,rgba(220,50,40,.35),transparent 70%),linear-gradient(180deg,#171112,#2a1412);border-bottom:2px solid #d8352a;font-family:Inter,system-ui,-apple-system,'Segoe UI',Arial,sans-serif}"+
  ".sb:hover .sb-go{background:#fff;color:#c4271d}"+
  ".sb-in{max-width:1180px;margin:0 auto;padding:0 16px 14px;display:flex;align-items:flex-end;justify-content:center;gap:clamp(14px,3vw,40px);flex-wrap:wrap}"+
  ".sb-tags{display:flex;align-items:flex-start;justify-content:center;gap:clamp(1px,.4vw,5px)}"+
  ".sb-t{width:clamp(30px,6.6vw,80px);height:auto;transform-origin:50% 0;animation:sbsw 3.2s ease-in-out infinite;filter:drop-shadow(0 4px 5px rgba(0,0,0,.45));display:block;overflow:visible}"+
  ".sb-txt{display:flex;flex-direction:column;align-items:center;gap:6px;padding-top:12px;text-align:center}"+
  ".sb-big{font-weight:800;font-size:clamp(24px,3.2vw,40px);line-height:1.05;letter-spacing:-.01em;text-wrap:balance}"+
  ".sb-big b{color:#ff4a3d}"+
  ".sb-sub{font-size:clamp(13px,1.5vw,16px);color:#e9d6d2}"+
  ".sb-go{display:inline-block;margin-top:2px;padding:8px 18px;border-radius:999px;background:#d8352a;color:#fff;font-weight:700;font-size:14px;transition:.2s}"+
  "@keyframes sbsw{0%,100%{transform:rotate(var(--r0,-4deg))}50%{transform:rotate(var(--r1,4deg))}}"+
  ".nav-sale{color:#ff3b30!important;font-weight:800;letter-spacing:.02em;animation:sbfl 1.3s steps(1,end) infinite;text-shadow:0 0 10px rgba(255,59,48,.65)}"+
  "@keyframes sbfl{0%,100%{opacity:1}45%{opacity:1}50%{opacity:.25}60%{opacity:1}75%{opacity:.4}85%{opacity:1}}"+
  "@media(prefers-reduced-motion:reduce){.sb-t,.nav-sale{animation:none}}";
  var st=d.createElement("style");st.textContent=css;d.head.appendChild(st);

  var letters="РАСПРОДАЖА".split(""),tags="";
  letters.forEach(function(ch,i){
    var r0=(i%2?4:-4)+((i*37)%5-2),r1=-r0,dl=(-(i*0.37)).toFixed(2);
    tags+='<svg class="sb-t" viewBox="0 0 60 130" style="--r0:'+r0+'deg;--r1:'+r1+'deg;animation-delay:'+dl+'s" aria-hidden="true">'+
    '<defs><linearGradient id="sbg'+i+'" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e8402f"/><stop offset="1" stop-color="#b01f17"/></linearGradient></defs>'+
    '<line x1="30" y1="-40" x2="30" y2="26" stroke="#0a0a0a" stroke-width="1.6"/>'+
    '<polygon points="20,24 40,24 56,44 56,126 4,126 4,44" fill="url(#sbg'+i+')" stroke="#8f1710" stroke-width="1" stroke-linejoin="round"/>'+
    '<circle cx="30" cy="36" r="7.5" fill="#f3f3f3" stroke="#9a9a9a" stroke-width="1.5"/><circle cx="30" cy="36" r="3.6" fill="#2a1412"/>'+
    '<text x="30" y="110" text-anchor="middle" font-family="Georgia,\'Times New Roman\',serif" font-weight="700" font-size="58" fill="#fff">'+ch+'</text></svg>';
  });
  var b=d.createElement("a");b.className="sb";b.href=href;b.setAttribute("aria-label","Распродажа 11.11 - 13.11. Перейти к предложениям");
  b.innerHTML='<div class="sb-in"><div class="sb-tags">'+tags+'</div><div class="sb-txt"><div class="sb-big">Распродажа <b>11.11 – 13.11</b></div><div class="sb-sub">Скидки до 50% на Школу, консультации и тест</div><span class="sb-go">Смотреть предложения →</span></div></div>';
  function place(){
    if(!onSale)d.body.insertBefore(b,d.body.firstChild);
    var ul=d.querySelector("header .nav ul, header nav ul");
    if(ul){var li=d.createElement("li"),a=d.createElement("a");a.href=href;a.textContent="Распродажа";a.className="nav-sale";li.appendChild(a);ul.insertBefore(li,ul.firstChild)}
  }
  if(d.body)place();else d.addEventListener("DOMContentLoaded",place);
})();
