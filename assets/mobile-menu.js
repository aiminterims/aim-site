/* Кнопка меню для телефонов и планшетов: на всех страницах сайта АИМ. */
(function(){
  if(window.__aimMenu)return;window.__aimMenu=1;
  var d=document;
  var L=(d.documentElement.lang||"ru").slice(0,2),LP=/^(en|kk|uz|hy|az)$/.test(L)?"/"+L:"";
  var TR={"ru": {"i": ["Мероприятия", "Продукты", "Собственникам", "Школа", "О нас", "Команда", "Партнёры", "Контакты", "Обсудить задачу"], "a": "Меню", "b": "Меню сайта", "alt": "Ассоциация Интерим Менеджеров"}, "en": {"i": ["Events", "Products", "For owners", "School", "About us", "Team", "Partners", "Contacts", "Discuss your task"], "a": "Menu", "b": "Site menu", "alt": "Association of Interim Managers"}, "kk": {"i": ["Іс-шаралар", "Өнімдер", "Меншік иелеріне", "Мектеп", "Біз туралы", "Команда", "Серіктестер", "Байланыс", "Міндетті талқылау"], "a": "Мәзір", "b": "Сайт мәзірі", "alt": "Интерим-менеджерлер қауымдастығы"}, "uz": {"i": ["Tadbirlar", "Mahsulotlar", "Biznes egalariga", "Maktab", "Biz haqimizda", "Jamoa", "Hamkorlar", "Aloqa", "Vazifani muhokama qilish"], "a": "Menyu", "b": "Sayt menyusi", "alt": "Interim menejerlar assotsiatsiyasi"}, "hy": {"i": ["Միջոցառումներ", "Ծառայություններ", "Սեփականատերերին", "Դպրոց", "Մեր մասին", "Թիմ", "Գործընկերներ", "Կոնտակտներ", "Քննարկել խնդիրը"], "a": "Մենյու", "b": "Կայքի մենյու", "alt": "Ինտերիմ մենեջերների ասոցիացիա"}, "az": {"i": ["Tədbirlər", "Məhsullar", "Biznes sahiblərinə", "Məktəb", "Haqqımızda", "Komanda", "Tərəfdaşlar", "Əlaqə", "Tapşırığı müzakirə edin"], "a": "Menyu", "b": "Sayt menyusi", "alt": "İnterim Menecerlər Assosiasiyası"}};
  var tr=TR[L]||TR.ru,U=["/#events","/products/","/#owners","/school/","/#about","/#team","/#partners","/#contacts"];
  var items=U.map(function(u,k){return [tr.i[k],(/^\/(products|school)\/|^\/#/.test(u)?LP:"")+u]});
  var css=
  ".am-btn{display:none;flex:0 0 auto;width:44px;height:44px;border-radius:12px;border:1px solid rgba(244,242,238,.28);background:rgba(244,242,238,.06);cursor:pointer;padding:0;align-items:center;justify-content:center;-webkit-tap-highlight-color:transparent;margin-left:12px}"+
  ".am-btn i,.am-btn i:before,.am-btn i:after{display:block;width:22px;height:2.5px;border-radius:2px;background:#f4f2ee;position:relative;transition:.2s}"+
  ".am-btn i:before,.am-btn i:after{content:'';position:absolute;left:0}.am-btn i:before{top:-7px}.am-btn i:after{top:7px}"+
  ".am-open .am-btn i{background:transparent}.am-open .am-btn i:before{top:0;transform:rotate(45deg)}.am-open .am-btn i:after{top:0;transform:rotate(-45deg)}"+
  ".am-bar{display:none;position:sticky;top:0;z-index:30;height:64px;align-items:center;justify-content:space-between;padding:0 max(16px,env(safe-area-inset-right,0px)) 0 max(16px,env(safe-area-inset-left,0px));background:#1c1c1e;border-bottom:1px solid #46464b}"+
  ".am-bar img{height:40px;width:auto;display:block}"+
  ".am-pan{display:none;position:fixed;left:0;right:0;bottom:0;top:var(--am-top,70px);z-index:15;background:rgba(28,28,30,.98);overflow:auto;padding:14px max(20px,env(safe-area-inset-right,0px)) 32px max(20px,env(safe-area-inset-left,0px));font-family:Inter,system-ui,-apple-system,'Segoe UI',Arial,sans-serif}"+
  ".am-open .am-pan{display:block}.am-open{overflow:hidden}"+
  ".am-pan a{display:block;color:#f4f2ee;text-decoration:none;font-weight:700;font-size:22px;line-height:1.25;padding:15px 2px;border-bottom:1px solid rgba(244,242,238,.14)}"+
  ".am-pan a.cta{margin-top:22px;border:0;border-radius:999px;background:#E8A33D;color:#1E1E20;text-align:center;font-size:18px;padding:15px 20px}"+
  "@media(max-width:980px){.am-btn{display:flex}.am-bar{display:flex}header.top{flex-wrap:nowrap;gap:10px;padding-right:0}header.top img{height:44px!important;width:auto!important;max-width:46vw}header.top .chip{flex:0 1 auto;font-size:12px;padding:6px 10px;text-align:center}}@media(max-width:640px){header .nav>.btn{display:none}}"+
  "@media(min-width:981px){html:not(.am-c) .am-pan{display:none!important}html:not(.am-c).am-open{overflow:auto}}"+
  "html.am-c .nav ul{display:none!important}html.am-c .am-btn{display:flex}";
  function init(){
    var st=d.createElement("style");st.textContent=css;d.head.appendChild(st);
    var b=d.createElement("button");b.className="am-btn";b.type="button";b.setAttribute("aria-label",tr.a);b.setAttribute("aria-expanded","false");b.innerHTML="<i></i>";
    var p=d.createElement("nav");p.className="am-pan";p.setAttribute("aria-label",tr.b);
    p.innerHTML=items.map(function(i){return '<a href="'+i[1]+'"'+(i[2]?' class="'+i[2]+'"':'')+'>'+i[0]+'</a>'}).join("")+
      '<a class="cta" href="https://t.me/AndreyAFomin" target="_blank" rel="noopener">'+tr.i[8]+'</a>';
    var root=d.documentElement,hdr=d.querySelector("body > header, header");
    var host=hdr&&(hdr.querySelector(".nav")||hdr);
    if(host){
      host.appendChild(b);
      if(getComputedStyle(hdr).position==="static")hdr.style.position="relative";
      hdr.style.zIndex="30";
    }else{
      hdr=d.createElement("div");hdr.className="am-bar";
      hdr.innerHTML='<a href="'+(LP||"/")+(LP?"/":"")+'"><img src="/assets/logo.png" alt="'+tr.alt+'"></a>';
      hdr.appendChild(b);
      var cs=getComputedStyle(d.body),g=function(k){return parseFloat(cs[k])||0};
      hdr.style.margin=(-(g("paddingTop")+g("marginTop")))+"px "+(-(g("paddingRight")+g("marginRight")))+"px 0 "+(-(g("paddingLeft")+g("marginLeft")))+"px";
      if(cs.display==="grid"){hdr.style.gridColumn="1/-1";hdr.style.alignSelf="start";hdr.style.justifySelf="stretch"}
      var sb=d.querySelector(".sb");
      if(sb&&sb.parentNode===d.body)hdr.style.marginTop="0";
      if(sb&&sb.parentNode===d.body)d.body.insertBefore(hdr,sb.nextSibling);else d.body.insertBefore(hdr,d.body.firstChild);
    }
    function set(o){
      if(o){
        var y=0,e=hdr;while(e){y+=e.offsetTop;e=e.offsetParent}
        window.scrollTo(0,Math.max(0,y));
        d.body.offsetHeight;
        root.style.setProperty("--am-top",Math.max(0,hdr.getBoundingClientRect().bottom)+"px");
      }
      root.classList.toggle("am-open",o);b.setAttribute("aria-expanded",o?"true":"false");
    }
    b.addEventListener("click",function(){set(!root.classList.contains("am-open"))});
    p.addEventListener("click",function(e){if(e.target.closest("a"))set(false)});
    d.addEventListener("keydown",function(e){if(e.key==="Escape")set(false)});
    function fit(){
      root.classList.remove("am-c");
      if(window.innerWidth<=980)return;
      var n=hdr&&(hdr.querySelector(".nav")||hdr);if(!n)return;
      var kids=n.children,last=kids[kids.length-1],nr=n.getBoundingClientRect(),over=root.scrollWidth>root.clientWidth+1;
      for(var i=0;i<kids.length;i++){var r=kids[i].getBoundingClientRect();if(r.width&&r.right>nr.right+1)over=true}
      if(over)root.classList.add("am-c");
    }
    window.__aimFit=fit;
    window.addEventListener("resize",function(){fit();if(window.innerWidth>980&&!root.classList.contains("am-c"))set(false)});
    if(d.fonts&&d.fonts.ready)d.fonts.ready.then(fit);
    window.addEventListener("load",fit);
    d.body.appendChild(p);
  }
  if(d.body)init();else d.addEventListener("DOMContentLoaded",init);
  (function(){var s=d.createElement("script");s.src="/assets/lang.js";s.defer=true;(d.head||d.documentElement).appendChild(s)})();
})();
