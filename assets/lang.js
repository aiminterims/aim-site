/* Переключатель языка сайта АИМ: на каждой странице. Подключается из mobile-menu.js */
(function(){
  if(window.__aimLang)return;window.__aimLang=1;
  var d=document;
  var LANGS=[["ru","Русский","RU"],["en","English","EN"],["kk","Қазақша","KK"],["uz","Oʻzbekcha","UZ"],["hy","Հայերեն","HY"],["az","Azərbaycanca","AZ"]];
  var CUR=(d.documentElement.lang||"ru").slice(0,2);
  var TITLE={ru:"Язык",en:"Language",kk:"Тіл",uz:"Til",hy:"Լեզու",az:"Dil"};
  var path=location.pathname.replace(/index\.html$/,"");
  var m=path.match(/^\/(en|kk|uz|hy|az)(\/.*)?$/);
  var base=m?(m[2]||"/"):path;
  var TRANSLATED=["/","/school/","/products/"];
  function target(l){
    var home=l==="ru"?"/":"/"+l+"/";
    if(TRANSLATED.indexOf(base)<0)return home;
    return (l==="ru"?"":"/"+l)+base+(location.hash||"");
  }
  var css=
  ".al-w{position:relative;flex:0 0 auto;margin-left:12px;font-family:Inter,Manrope,system-ui,-apple-system,'Segoe UI',Arial,sans-serif}"+
  ".al-b{display:flex;align-items:center;gap:6px;height:44px;padding:0 12px;border-radius:12px;border:1px solid rgba(244,242,238,.28);background:rgba(244,242,238,.06);color:#f4f2ee;font:700 13px/1 inherit;font-family:inherit;cursor:pointer;-webkit-tap-highlight-color:transparent}"+
  ".al-b:hover{background:rgba(244,242,238,.12)}.al-b svg{width:18px;height:18px;flex:0 0 auto}"+
  ".al-l{display:none;position:absolute;right:0;top:calc(100% + 8px);min-width:180px;margin:0;padding:6px;background:#1c1c1e;border:1px solid #46464b;border-radius:14px;box-shadow:0 14px 40px rgba(0,0,0,.45);z-index:60}"+
  ".al-open .al-l{display:block}"+
  ".al-l a{display:flex!important;color:#f4f2ee!important;font-size:15px!important;justify-content:space-between;gap:14px;align-items:center;padding:11px 12px;border-radius:9px;color:#f4f2ee;text-decoration:none;font-weight:600;font-size:15px;white-space:nowrap}"+
  ".al-l a[aria-current=true]{color:#E8A33D!important}.al-l a:hover{background:rgba(244,242,238,.09)}.al-l a small{opacity:.55;font-weight:700;font-size:11px}"+
  ".al-l a[aria-current=true]{color:#E8A33D}"+
  ".al-fix{position:fixed;top:10px;right:12px;z-index:60;margin:0}"+
  "@media(max-width:980px){.al-w{margin-left:auto}.al-w+.am-btn{margin-left:8px}}"+
  "@media(max-width:640px){header .nav{gap:8px}.al-b span{display:none}.al-b{padding:0 11px}.al-w{margin-left:6px}.al-w+.am-btn{margin-left:6px}}";
  function init(){
    if(d.querySelector(".al-w"))return;
    var st=d.createElement("style");st.textContent=css;d.head.appendChild(st);
    var w=d.createElement("div");w.className="al-w";
    var b=d.createElement("button");b.type="button";b.className="al-b";b.setAttribute("aria-haspopup","true");b.setAttribute("aria-expanded","false");b.setAttribute("aria-label",TITLE[CUR]||"Language");
    b.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.7 3.9 5.7 3.9 9S14.6 18.3 12 21c-2.6-2.7-3.9-5.7-3.9-9S9.4 5.7 12 3z"/></svg><span>'+CUR.toUpperCase()+'</span>';
    var ul=d.createElement("div");ul.className="al-l";ul.setAttribute("role","menu");
    LANGS.forEach(function(x){
      var a=d.createElement("a");
      a.href=target(x[0]);a.hreflang=x[0];a.lang=x[0];a.setAttribute("role","menuitem");
      if(x[0]===CUR)a.setAttribute("aria-current","true");
      a.innerHTML=x[1]+"<small>"+x[2]+"</small>";
      a.addEventListener("click",function(){try{localStorage.setItem("aim_lang",x[0])}catch(e){}});
      ul.appendChild(a);
    });
    w.appendChild(b);w.appendChild(ul);
    var hdr=d.querySelector("body > header, header"),host=hdr&&(hdr.querySelector(".nav")||hdr)||d.querySelector(".am-bar");
    if(host){
      var mb=host.querySelector(".am-btn");
      if(mb)host.insertBefore(w,mb);else host.appendChild(w);
    }else{w.classList.add("al-fix");d.body.appendChild(w)}
    b.addEventListener("click",function(e){e.stopPropagation();var o=!w.classList.contains("al-open");w.classList.toggle("al-open",o);b.setAttribute("aria-expanded",o?"true":"false")});
    d.addEventListener("click",function(e){if(!w.contains(e.target)){w.classList.remove("al-open");b.setAttribute("aria-expanded","false")}});
    d.addEventListener("keydown",function(e){if(e.key==="Escape"){w.classList.remove("al-open");b.setAttribute("aria-expanded","false")}});
    window.addEventListener("hashchange",function(){ul.querySelectorAll("a").forEach(function(a,i){a.href=target(LANGS[i][0])})});
  }
  function go(){init();if(window.__aimFit)window.__aimFit();else window.dispatchEvent(new Event("resize"))}
  if(d.readyState==="loading")d.addEventListener("DOMContentLoaded",go);else go();
})();
