function i() {
  this.D = function () {
    const t = h.atan(this.i / this.d);
    l.save(),
      l.translate(this.b, this.a),
      l.rotate(-t),
      l.scale(this.e, this.e * h.max(1, h.pow(this.j, 0.7) / 15)),
      l.drawImage(m, -v / 2, -v / 2),
      l.restore();
  };
}

window;
const h = Math;
const r = h.random;
const a = document;
const o = Date.now;
(e = (t) => {
  l.clearRect(0, 0, _, f), l.fill(), requestAnimationFrame(e);
  const i = 0.001 * y.et;
  y.r();
  const s = L.et * g;
  for (let n = 0; n < C.length; ++n) {
    const t = C[n];
    (t.i = h.sin(s + t.g) * t.h),
      (t.j = h.sqrt(t.i * t.i + t.f)),
      (t.a += t.d * i),
      (t.b += t.i * i),
      t.a > w && (t.a = -u),
      t.b > b && (t.b = -u),
      t.b < -u && (t.b = b),
      t.D();
  }
}),
  (s = (t) => {
    for (let e = 0; e < p; ++e) (C[e].a = r() * (f + u)), (C[e].b = r() * _);
  }),
  (n = (t) => {
    (c.width = _ = innerWidth),
      (c.height = f = innerHeight),
      (w = f + u),
      (b = _ + u),
      s();
  });

class d {
  constructor(t, e = !0) {
    (this._ts = o()),
      (this._p = !0),
      (this._pa = o()),
      (this.d = t),
      e && this.s();
  }

  get et() {
    return this.ip ? this._pa - this._ts : o() - this._ts;
  }

  get rt() {
    return h.max(0, this.d - this.et);
  }

  get ip() {
    return this._p;
  }

  get ic() {
    return this.et >= this.d;
  }

  s() {
    return (this._ts = o() - this.et), (this._p = !1), this;
  }

  r() {
    return (this._pa = this._ts = o()), this;
  }

  p() {
    return (this._p = !0), (this._pa = o()), this;
  }

  st() {
    return (this._p = !0), this;
  }
}

const c = a.createElement("canvas");
(H = c.style),
  (H.position = "fixed"),
  (H.left = 0),
  (H.top = 0),
  (H.width = "100vw"),
  (H.height = "100vh"),
  (H.zIndex = "100000"),
  (H.pointerEvents = "none"),
  a.body.insertBefore(c, a.body.children[0]);
const l = c.getContext("2d");
const p = 300;
const g = 5e-4;
const u = 20;
let _ = (c.width = innerWidth);
let f = (c.height = innerHeight);
let w = f + u;
let b = _ + u;
const v = 15.2;
const m = a.createElement("canvas");
const E = m.getContext("2d");
const x = E.createRadialGradient(7.6, 7.6, 0, 7.6, 7.6, 7.6);
x.addColorStop(0, "hsla(255,255%,255%,1)"),
  x.addColorStop(1, "hsla(255,255%,255%,0)"),
  (E.fillStyle = x),
  E.fillRect(0, 0, v, v);
const y = new d(0, !0);
const C = [];
const L = new d(0, !0);
for (let j = 0; j < p; ++j) {
  const t = new i();
  (t.a = r() * (f + u)),
    (t.b = r() * _),
    (t.c = 1 * (3 * r() + 0.8)),
    (t.d = 0.1 * h.pow(t.c, 2.5) * 50 * (2 * r() + 1)),
    (t.d = t.d < 65 ? 65 : t.d),
    (t.e = t.c / 7.6),
    (t.f = t.d * t.d),
    (t.g = (r() * h.PI) / 1.3),
    (t.h = 15 * t.c),
    (t.i = 0),
    (t.j = 0),
    C.push(t);
}
s(),
  (EL = a.addEventListener),
  EL("visibilitychange", () => setTimeout(n, 100), !1),
  EL("resize", n, !1),
  e();
