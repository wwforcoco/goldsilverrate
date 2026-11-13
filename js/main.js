(function(){
var T=11.664,M=T/12,R=M/8;
var el=document.getElementById('rates');
if(!el)return;
var d=JSON.parse(el.textContent);
var metals={
 psl:{n:'Silver (PSL bar)',s:d.silver.psl_tola_sell,b:d.silver.psl_tola_buy},
 rawa:{n:'Silver (Rawa)',s:d.silver.rawa_tola_sell,b:d.silver.rawa_tola_buy},
 g24:{n:'Gold 24K',s:d.gold['24k_tola_sell'],b:d.gold['24k_tola_buy']},
 g22:{n:'Gold 22K',s:d.gold['22k_tola_sell'],b:d.gold['22k_tola_sell']*d.gold['24k_tola_buy']/d.gold['24k_tola_sell']},
 g21:{n:'Gold 21K',s:d.gold['21k_tola_sell'],b:d.gold['21k_tola_sell']*d.gold['24k_tola_buy']/d.gold['24k_tola_sell']},
 g18:{n:'Gold 18K',s:d.gold['24k_tola_sell']*0.75,b:d.gold['24k_tola_buy']*0.75}
};
var units={gram:1,tola:T,masha:M,ratti:R,kg:1000};
function pk(n){return 'Rs '+Math.round(n).toLocaleString('en-US')}
function num(n){return (Math.round(n*1000)/1000).toLocaleString('en-US',{maximumFractionDigits:3})}
function $(i){return document.getElementById(i)}
var cm=$('calc-metal');
if(cm){
 var cu=$('calc-unit'),cq=$('calc-qty'),co=$('calc-out');
 var run=function(){
  var m=metals[cm.value],q=parseFloat(cq.value)||0,g=q*units[cu.value];
  var tolas=g/T;
  co.innerHTML='<p>'+num(q)+' '+cu.options[cu.selectedIndex].text.toLowerCase()+' of '+m.n+' = '+num(g)+' grams ('+num(tolas)+' tola)</p>'+
  '<p>Selling price: <strong>'+pk(tolas*m.s)+'</strong></p><p>Buying price: <strong>'+pk(tolas*m.b)+'</strong></p>';
 };
 cm.onchange=cu.onchange=run;cq.oninput=run;run();
}
var cv=$('cv-val');
if(cv){
 var cf=$('cv-unit'),cvo=$('cv-out');
 var run2=function(){
  var g=(parseFloat(cv.value)||0)*units[cf.value];
  cvo.innerHTML='<p><strong>'+num(g)+'</strong> grams</p><p>'+num(g/T)+' tola</p><p>'+num(g/M)+' masha</p><p>'+num(g/R)+' ratti</p><p>'+num(g/1000)+' kg</p>';
 };
 cv.oninput=cf.onchange=run2;run2();
}
var jm=$('jw-metal');
if(jm){
 var jw=$('jw-wt'),jk=$('jw-kaat'),jz=$('jw-maz'),jo=$('jw-out');
 var run3=function(){
  var m=metals[jm.value],w=parseFloat(jw.value)||0,k=parseFloat(jk.value)||0,z=parseFloat(jz.value)||0;
  var metal=w*m.s,kaat=w*(k/12)*m.s,mz=w*z,tot=metal+kaat+mz;
  jo.innerHTML='<p>Metal value: '+pk(metal)+'</p><p>Kaat (wastage): '+pk(kaat)+'</p><p>Mazdoori (making): '+pk(mz)+'</p><p>Estimated total: <strong>'+pk(tot)+'</strong></p>';
 };
 jm.onchange=jw.oninput=jk.oninput=jz.oninput=run3;run3();
}
})();
