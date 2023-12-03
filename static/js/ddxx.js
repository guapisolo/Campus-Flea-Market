!function(){
    function Nn(n,e,t){return n.getAttribute(e)||t}
    function e(n){return document.getElementsByTagName(n)}
    
    /*在m数组中修改颜色*/
    var m=new Array(t(66,66,66),t(128,128,128));
    /*在ptcnt的值是点数*/
    var ptcnt=150;
    /*在opct的值是透明度*/
    var opct=0.9;
    /*在LWnum的值是线粗细*/
    var LWnum=0.8;
    /*在PWnum的值是点粗细*/
    var PWnum=2;
    /*设置点的颜色*/
    var PColor='#777';
    /*设置脱离速度*/
    var Rv=0.03;
    
    function t(r,g,b){
        var t=e("script"),o=t.length,i=t[o-1];
        return{l:o,z:Nn(i,"zIndex",-1),o:Nn(i,"opacity",opct),c:Nn(i,"color",r+","+g+","+b),n:Nn(i,"count",ptcnt)}
    }
    var c,a,u=document.createElement("canvas"),l=u.getContext("2d");
    var vry=m.length;
    var d=m[0].l,pts=new Array();
    function rd(n){
        return Math.floor((Math.random()*(n)));
    }
    function o(){
        c=u.width=window.innerWidth||document.documentElement.clientWidth||document.body.clientWidth,
        a=u.height=window.innerHeight||document.documentElement.clientHeight||document.body.clientHeight
    }
    function gt(x){
        return m[x];
    }
    var pts=new Array();
    function i(){
        l.clearRect(0,0,c,a);
        var n,e,t,o,u,d,x=[w].concat(y);
        y.forEach(
            function(i){
                for(i.x+=i.xa,i.y+=i.ya,i.xa*=i.x>c||i.x<0?-1:1,i.ya*=i.y>a
                ||i.y<0?-1:1,l.fillStyle=PColor,l.fillRect(i.x-PWnum/2,i.y-PWnum/2,PWnum,PWnum),e=0;e<x.length;e++)
                    n=x[e],i!==n&&null!==n.x&&null!==n.y&&(o=i.x-n.x,u=i.y-n.y,d=o*o+u*u,d<n.max&&(n===w&&d>=n.max/2&&(i.x-=Rv*o,i.y-=Rv*u),
                    t=(n.max-d)/n.max,l.beginPath(),l.lineWidth=t*LWnum,l.strokeStyle="rgba("+gt(i.tp).c+","+(t+.2)+")",l.moveTo(i.x,i.y),l.lineTo(n.x,n.y),l.stroke()));
                x.splice(x.indexOf(i),1)}),r(i)
    }
    var r=window.requestAnimationFrame||window.webkitRequestAnimationFrame||window.mozRequestAnimationFrame||window.oRequestAnimationFrame||window.msRequestAnimationFrame||
        function(n){
            window.setTimeout(n,1e3/45)},x=Math.random,w={x:null,y:null,max:2e4};
            u.id=d,u.style.cssText="position:fixed;top:0;left:0;z-index:"+gt(rd(vry)).z+";opacity:"+gt(rd(vry)).o,e("body")[0].appendChild(u),
            o(),window.onresize=o,window.onmousemove=function(n){n=n||window.event,w.x=n.clientX,w.y=n.clientY},window.onmouseout=
            function(){w.x=null,w.y=null};for(var y=[],s=0;ptcnt>s;s++){var f=x()*c,h=x()*a,g=2*x()-1,p=2*x()-1;y.push({x:f,y:h,xa:g,ya:p,max:6e3,tp:rd(vry)})}setTimeout(function(){i()},100)
        }();