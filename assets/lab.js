(() => {
  const $ = id => document.getElementById(id);
  const canvas = $('lp-plot');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  function text(c, value, x, y, color = '#dce5ee') {
    c.fillStyle = color; c.font = '18px system-ui'; c.fillText(value, x, y);
  }
  function axes(c, w, h, xLabel, yLabel) {
    c.clearRect(0, 0, w, h); c.strokeStyle = '#607488'; c.lineWidth = 2;
    c.beginPath(); c.moveTo(65, 30); c.lineTo(65, h-55); c.lineTo(w-35, h-55); c.stroke();
    text(c, xLabel, w-85, h-15); text(c, yLabel, 15, 30);
  }
  function lp() {
    const b = +$('capacity').value;
    $('capacity-value').textContent = b.toFixed(2);
    const x = Math.min(2, b), y = Math.min(3, b-x), value = 3*x+2*y;
    $('lp-result').textContent = `Optimal (x, y) = (${x.toFixed(2)}, ${y.toFixed(2)}); profit = ${value.toFixed(2)}.`;
    const price = Math.abs(b-2)<1e-8 ? '[2, 3]' : Math.abs(b-5)<1e-8 ? '[0, 2]' : b<2 ? '3' : b<5 ? '2' : '0';
    $('lp-price').textContent = `Optimal resource multiplier: ${price}.`;
    const w=canvas.width, h=canvas.height, sx=(w-120)/4, sy=(h-110)/4;
    const X=v=>65+sx*v, Y=v=>h-55-sy*v;
    axes(ctx,w,h,'x','y');
    const candidates=[[0,0],[2,0],[2,3],[0,3],[b,0],[0,b],[2,b-2],[b-3,3]];
    const points=candidates.filter(([a,c])=>a>=-1e-8&&c>=-1e-8&&a<=2+1e-8&&c<=3+1e-8&&a+c<=b+1e-8);
    const mean=points.reduce((s,p)=>[s[0]+p[0]/points.length,s[1]+p[1]/points.length],[0,0]);
    points.sort((a,c)=>Math.atan2(a[1]-mean[1],a[0]-mean[0])-Math.atan2(c[1]-mean[1],c[0]-mean[0]));
    ctx.fillStyle='#23584f';ctx.beginPath();points.forEach(([a,c],i)=>i?ctx.lineTo(X(a),Y(c)):ctx.moveTo(X(a),Y(c)));ctx.closePath();ctx.fill();
    ctx.strokeStyle='#82d6c6';ctx.setLineDash([8,6]);ctx.beginPath();ctx.moveTo(X(2),Y(0));ctx.lineTo(X(2),Y(4));ctx.moveTo(X(0),Y(3));ctx.lineTo(X(4),Y(3));ctx.stroke();ctx.setLineDash([]);
    const a=Math.max(0,b-4), d=Math.min(4,b);
    ctx.strokeStyle='#9bc8ff';ctx.beginPath();ctx.moveTo(X(a),Y(b-a));ctx.lineTo(X(d),Y(b-d));ctx.stroke();
    ctx.fillStyle='#f2ce79';ctx.beginPath();ctx.arc(X(x),Y(y),7,0,2*Math.PI);ctx.fill();
    for(let i=0;i<=4;i++){text(ctx,String(i),X(i)-5,Y(0)+26);if(i)text(ctx,String(i),35,Y(i)+6);}
    text(ctx,`3x + 2y = ${value.toFixed(2)}`,X(x)+12,Y(y)-12,'#f2ce79');
  }
  function gradient() {
    const kappa=+$('conditioning').value, count=+$('iterations').value;
    $('conditioning-value').textContent=kappa;$('iterations-value').textContent=count;
    const c=$('gradient-plot'),g=c.getContext('2d'),w=c.width,h=c.height;
    const initial=.5*(1+kappa),values=[1];let first=1,second=1;
    for(let k=0;k<count;k++){first*=1-1/kappa;second*=0;values.push(.5*(first*first+kappa*second*second)/initial);}
    $('gradient-result').textContent=`Step α = ${(1/kappa).toPrecision(4)}; final objective = ${(values.at(-1)*initial).toExponential(4)}; relative objective = ${values.at(-1).toExponential(4)}.`;
    axes(g,w,h,'step','log₁₀ relative objective');
    const X=i=>65+(w-110)*i/count,Y=v=>h-55-(h-110)*(Math.max(-12,Math.log10(Math.max(1e-12,v)))+12)/12;
    g.strokeStyle='#82d6c6';g.lineWidth=3;g.beginPath();values.forEach((v,i)=>i?g.lineTo(X(i),Y(v)):g.moveTo(X(i),Y(v)));g.stroke();
    for(let i=0;i<=12;i+=3){text(g,String(-i),20,Y(10**(-i))+5);}
    text(g,'0',65,h-25);text(g,String(count),w-65,h-25);text(g,'Values below 10⁻¹² are clipped on this plot.',100,h-80,'#9eafbf');
  }
  $('capacity').addEventListener('input',lp);
  $('conditioning').addEventListener('input',gradient);$('iterations').addEventListener('input',gradient);
  lp();gradient();
})();
