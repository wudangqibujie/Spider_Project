import execjs
def create_cookie():
    a = execjs.compile(r"""
    eval(function(p, a, c, k, e, r) {
        e = function(c) {
            return (c < 62 ? '' : e(parseInt(c / 62))) + ((c = c % 62) > 35 ? String.fromCharCode(c + 29) : c.toString(36))
        }
        ;
        if ('0'.replace(0, e) == 0) {
            while (c--)
                r[e(c)] = k[c];
            k = [function(e) {
                return r[e] || e
            }
            ];
            e = function() {
                return '([efhj-pru-wzA-Y]|1\\w)'
            }
            ;
            c = 1
        }
        ;while (c--)
            if (k[c])
                p = p.replace(new RegExp('\\b' + e(c) + '\\b','g'), k[c]);
        return p
    }('f u(x,y){e M=(x&N)+(y&N);e 1f=(x>>16)+(y>>16)+(M>>16);h(1f<<16)|(M&N)}f 1g(O,P){h(O<<P)|(O>>>(32-P))}f C(q,a,b,x,s,t){h u(1g(u(u(a,q),u(x,t)),s),b)}f j(a,b,c,d,x,s,t){h C((b&c)|((~b)&d),a,b,x,s,t)}f k(a,b,c,d,x,s,t){h C((b&d)|(c&(~d)),a,b,x,s,t)}f l(a,b,c,d,x,s,t){h C(b^c^d,a,b,x,s,t)}f m(a,b,c,d,x,s,t){h C(c^(b|(~d)),a,b,x,s,t)}f D(x,w){x[w>>5]|=0x80<<(w%32);x[(((w+64)>>>9)<<4)+14]=w;e i;e Q;e R;e S;e T;e a=1732584193;e b=-271733879;e c=-1732584194;e d=271733878;v(i=0;i<x.n;i+=16){Q=a;R=b;S=c;T=d;a=j(a,b,c,d,x[i],7,-680876936);d=j(d,a,b,c,x[i+1],12,-389564586);c=j(c,d,a,b,x[i+2],17,606105819);b=j(b,c,d,a,x[i+3],22,-1044525330);a=j(a,b,c,d,x[i+4],7,-176418897);d=j(d,a,b,c,x[i+5],12,1200080426);c=j(c,d,a,b,x[i+6],17,-1473231341);b=j(b,c,d,a,x[i+7],22,-45705983);a=j(a,b,c,d,x[i+8],7,1770035416);d=j(d,a,b,c,x[i+9],12,-1958414417);c=j(c,d,a,b,x[i+10],17,-42063);b=j(b,c,d,a,x[i+11],22,-1990404162);a=j(a,b,c,d,x[i+12],7,1804603682);d=j(d,a,b,c,x[i+13],12,-40341101);c=j(c,d,a,b,x[i+14],17,-1502002290);b=j(b,c,d,a,x[i+15],22,1236535329);a=k(a,b,c,d,x[i+1],5,-165796510);d=k(d,a,b,c,x[i+6],9,-1069501632);c=k(c,d,a,b,x[i+11],14,643717713);b=k(b,c,d,a,x[i],20,-373897302);a=k(a,b,c,d,x[i+5],5,-701558691);d=k(d,a,b,c,x[i+10],9,38016083);c=k(c,d,a,b,x[i+15],14,-660478335);b=k(b,c,d,a,x[i+4],20,-405537848);a=k(a,b,c,d,x[i+9],5,568446438);d=k(d,a,b,c,x[i+14],9,-1019803690);c=k(c,d,a,b,x[i+3],14,-187363961);b=k(b,c,d,a,x[i+8],20,1163531501);a=k(a,b,c,d,x[i+13],5,-1444681467);d=k(d,a,b,c,x[i+2],9,-51403784);c=k(c,d,a,b,x[i+7],14,1735328473);b=k(b,c,d,a,x[i+12],20,-1926607734);a=l(a,b,c,d,x[i+5],4,-378558);d=l(d,a,b,c,x[i+8],11,-2022574463);c=l(c,d,a,b,x[i+11],16,1839030562);b=l(b,c,d,a,x[i+14],23,-35309556);a=l(a,b,c,d,x[i+1],4,-1530992060);d=l(d,a,b,c,x[i+4],11,1272893353);c=l(c,d,a,b,x[i+7],16,-155497632);b=l(b,c,d,a,x[i+10],23,-1094730640);a=l(a,b,c,d,x[i+13],4,681279174);d=l(d,a,b,c,x[i],11,-358537222);c=l(c,d,a,b,x[i+3],16,-722521979);b=l(b,c,d,a,x[i+6],23,76029189);a=l(a,b,c,d,x[i+9],4,-640364487);d=l(d,a,b,c,x[i+12],11,-421815835);c=l(c,d,a,b,x[i+15],16,530742520);b=l(b,c,d,a,x[i+2],23,-995338651);a=m(a,b,c,d,x[i],6,-198630844);d=m(d,a,b,c,x[i+7],10,1126891415);c=m(c,d,a,b,x[i+14],15,-1416354905);b=m(b,c,d,a,x[i+5],21,-57434055);a=m(a,b,c,d,x[i+12],6,1700485571);d=m(d,a,b,c,x[i+3],10,-1894986606);c=m(c,d,a,b,x[i+10],15,-1051523);b=m(b,c,d,a,x[i+1],21,-2054922799);a=m(a,b,c,d,x[i+8],6,1873313359);d=m(d,a,b,c,x[i+15],10,-30611744);c=m(c,d,a,b,x[i+6],15,-1560198380);b=m(b,c,d,a,x[i+13],21,1309151649);a=m(a,b,c,d,x[i+4],6,-145523070);d=m(d,a,b,c,x[i+11],10,-1120210379);c=m(c,d,a,b,x[i+2],15,718787259);b=m(b,c,d,a,x[i+9],21,-343485551);a=u(a,Q);b=u(b,R);c=u(c,S);d=u(d,T)}h[a,b,c,d]}f U(o){e i;e p=\'\';e 1h=o.n*32;v(i=0;i<1h;i+=8){p+=String.fromCharCode((o[i>>5]>>>(i%32))&1i)}h p}f F(o){e i;e p=[];p[(o.n>>2)-1]=1j;v(i=0;i<p.n;i+=1){p[i]=0}e 1k=o.n*8;v(i=0;i<1k;i+=8){p[i>>5]|=(o.1l(i/8)&1i)<<(i%32)}h p}f 1m(s){h U(D(F(s),s.n*8))}f rstrHMAC(G,V){e i;e A=F(G);e H=[];e I=[];e W;H[15]=I[15]=1j;z(A.n>16){A=D(A,G.n*8)}v(i=0;i<16;i+=1){H[i]=A[i]^0x36363636;I[i]=A[i]^0x5C5C5C5C}W=D(H.1n(F(V)),1o+V.n*8);h U(D(I.1n(W),1o+128))}f 1p(o){e X=\'0123456789abcdef\';e p=\'\';e x;e i;v(i=0;i<o.n;i+=1){x=o.1l(i);p+=X.Y((x>>>4)&1q)+X.Y(x&1q)}h p}f 1r(o){h unescape(encodeURIComponent(o))}f 1s(s){h 1m(1r(s))}f 1t(s){h 1p(1s(s))}f 1u(){e 18="";e 19="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";e w=J.1v(J.1w()*2);v(e i=0;i<w;i++){18+=19.Y(J.1v(J.1w()*19.n))}h 18}f 1x(s){s=s.1y(/[a-zA-Z]/g,\'#\');e E=s.split(\'\');v(e i=0;i<E.n;i++){z(E[i]==\'#\'){E[i]=1u()}}h E.join(\'\')}f anti(1z,G){e 1A=1t(1z);h 1x(1A)}f xredirect(1a,1B,r){e K=new Date();K.setTime(K.getTime()+2592000000);e 1b="; 1b="+K.toUTCString();1C.1c=1a+"="+1B+1b+"; path=/";z(1C.1c.1D(1a)===-1&&navigator.cookieEnabled){alert(\'请修改浏览器设置,允许1c缓存\')}1E{z(r==\'\'){e r=B.1F;z(B.1d!=\'L:\'){r=\'L:\'+1G.B.1F.1H(1G.B.1d.n)}}1E{z(B.1d!=\'L:\'){r=\'L:\'+r}}e 1e=r.1D(\'#\');z(1e!==-1){r=r.1H(0,1e)}B.1y(r)}}', [], 106, '||||||||||||||var|function||return||ff|gg|hh|ii|length|input|output||url|||safeAdd|for|len|||if|bkey|location|cmn|binl|arr|rstr2binl|key|ipad|opad|Math|date|https|lsw|0xFFFF|num|cnt|olda|oldb|oldc|oldd|binl2rstr|data|hash|hexTab|charAt||||||||||text|possible|name|expires|cookie|protocol|ulen|msw|bitRotateLeft|length32|0xFF|undefined|length8|charCodeAt|rstr|concat|512|rstr2hex|0x0F|str2rstrUTF8|raw|hex|uid|floor|random|charRun|replace|string|estring|value|document|indexOf|else|href|window|substring'.split('|'), 0, {}));
    var value = anti('ghRAqwHwTYXfHCW59+YnqnQHkDCNjwviVKBL8Q7Wzjc=', '268188568723544');
    var name = 'antipas';
    var url = '';
    xredirect(name, value, url, 'https://');
    function A(){return value;}
    """)
    print(a.call("A"))
    return a.call("A")

def create_cooki_pool():
    f = open("cookie_pool.txt","w")
    for i in range(100):
        cooki = create_cookie()
        f.write(cooki+"\n")
    f.close()
if __name__ == '__main__':
    create_cooki_pool()

