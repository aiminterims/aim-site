/* Кнопка меню для телефонов и планшетов: на всех страницах сайта АИМ. */
(function(){
  if(window.__aimMenu)return;window.__aimMenu=1;
  var d=document;
  var sale=Date.now()<Date.parse("2026-11-14T00:00:00+03:00");
  var items=[
    sale?["Распродажа","/sale/","sale"]:null,
    ["Мероприятия","/#events"],["Собственникам","/#owners"],["Школа","/school/"],
    ["Тест: готов ли я стать интеримом?","/test/"],["О нас","/#about"],["Команда","/#team"],
    ["Партнёры","/#partners"],["Контакты","/#contacts"]
  ].filter(Boolean);
  var css=
  ".am-btn{display:none;position:fixed;top:14px;right:max(14px,env(safe-area-inset-right,0px));z-index:2147483000;width:46px;height:46px;border-radius:12px;border:1px solid rgba(244,242,238,.28);background:rgba(35,35,37,.94);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);box-shadow:0 4px 14px rgba(0,0,0,.4);cursor:pointer;padding:0;align-items:center;justify-content:center;-webkit-tap-highlight-color:transparent}"+
  ".am-btn i,.am-btn i:before,.am-btn i:after{display:block;width:22px;height:2.5px;border-radius:2px;background:#f4f2ee;position:relative;transition:.2s}"+
  ".am-btn i:before,.am-btn i:after{content:'';position:absolute;left:0}.am-btn i:before{top:-7px}.am-btn i:after{top:7px}"+
  ".am-open .am-btn i{background:transparent}.am-open .am-btn i:before{top:0;transform:rotate(45deg)}.am-open .am-btn i:after{top:0;transform:rotate(-45deg)}"+
  ".am-pan{display:none;position:fixed;inset:0;z-index:2147482999;background:rgba(28,28,30,.98);overflow:auto;padding:78px max(20px,env(safe-area-inset-right,0px)) 32px max(20px,env(safe-area-inset-left,0px));font-family:Inter,system-ui,-apple-system,'Segoe UI',Arial,sans-serif}"+
  ".am-open .am-pan{display:block}.am-open{overflow:hidden}"+
  ".am-pan a{display:block;color:#f4f2ee;text-decoration:none;font-weight:700;font-size:22px;line-height:1.25;padding:15px 2px;border-bottom:1px solid rgba(244,242,238,.14)}"+
  ".am-pan a.sale{color:#ff3b30;text-shadow:0 0 10px rgba(255,59,48,.55);animation:amfl 1.3s steps(1,end) infinite}"+
  ".am-pan a.cta{margin-top:22px;border:0;border-radius:999px;background:#E8A33D;color:#1E1E20;text-align:center;font-size:18px;padding:15px 20px}"+
  "@keyframes amfl{0%,100%{opacity:1}45%{opacity:1}50%{opacity:.3}60%{opacity:1}75%{opacity:.45}85%{opacity:1}}"+
  "@media(max-width:980px){.am-btn{display:flex}.sb-in{padding-right:70px!important}header .nav{padding-right:62px!important;box-sizing:border-box}header.top{padding-right:62px;box-sizing:border-box}}"+
  "@media(min-width:981px){.am-pan{display:none!important}.am-open{overflow:auto}}"+
  "@media(prefers-reduced-motion:reduce){.am-pan a.sale{animation:none}}";
  function init(){
    var st=d.createElement("style");st.textContent=css;d.head.appendChild(st);
    var b=d.createElement("button");b.className="am-btn";b.type="button";b.setAttribute("aria-label","Меню");b.setAttribute("aria-expanded","false");b.innerHTML="<i></i>";
    var p=d.createElement("nav");p.className="am-pan";p.setAttribute("aria-label","Меню сайта");
    p.innerHTML=items.map(function(i){return '<a href="'+i[1]+'"'+(i[2]?' class="'+i[2]+'"':'')+'>'+i[0]+'</a>'}).join("")+
      '<a class="cta" href="https://t.me/AndreyAFomin" target="_blank" rel="noopener">Обсудить задачу</a>';
    var root=d.documentElement;
    function set(o){root.classList.toggle("am-open",o);b.setAttribute("aria-expanded",o?"true":"false")}
    b.addEventListener("click",function(){set(!root.classList.contains("am-open"))});
    p.addEventListener("click",function(e){if(e.target.closest("a"))set(false)});
    d.addEventListener("keydown",function(e){if(e.key==="Escape")set(false)});
    window.addEventListener("resize",function(){if(window.innerWidth>980)set(false)});
    d.body.appendChild(p);d.body.appendChild(b);
  }
  if(d.body)init();else d.addEventListener("DOMContentLoaded",init);
})();
