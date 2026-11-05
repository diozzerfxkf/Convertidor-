# Crea los widgets nativos de Android (grande 4x3 y chico 2x2) dentro del proyecto Capacitor.
# Lo ejecuta el workflow despues de "npx cap add android". No hace falta tocarlo.
import json, os, sys

PKG = json.load(open('capacitor.config.json'))['appId']
BASE = 'android/app/src/main'
JD = os.path.join(BASE, 'java', *PKG.split('.'))
RES = os.path.join(BASE, 'res')
F = {}

# ---------- DRAWABLES ----------
def shape(fill, radius, stroke=None, oval=False, grad=None):
    s = '<?xml version="1.0" encoding="utf-8"?>\n<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="%s">\n' % ('oval' if oval else 'rectangle')
    if grad:
        s += '  <gradient android:angle="%d" android:startColor="%s" android:endColor="%s"/>\n' % grad
    else:
        s += '  <solid android:color="%s"/>\n' % fill
    if not oval:
        s += '  <corners android:radius="%s"/>\n' % radius
    if stroke:
        s += '  <stroke android:width="1dp" android:color="%s"/>\n' % stroke
    return s + '</shape>\n'

F[RES + '/drawable/bg_widget.xml'] = shape(None, '24dp', '#1AFFFFFF', grad=(315, '#2A2B30', '#141518'))
F[RES + '/drawable/bg_orange.xml'] = shape(None, '16dp', grad=(315, '#FF8A4C', '#EE5A1E'))
F[RES + '/drawable/bg_pill.xml'] = shape('#101114', '30dp', '#18FFFFFF')
F[RES + '/drawable/bg_key.xml'] = shape('#16FFFFFF', '10dp')
F[RES + '/drawable/bg_key_o.xml'] = shape('#33FF6A2B', '10dp')
F[RES + '/drawable/bg_swap.xml'] = shape('#FF6A2B', '0dp', oval=True)
F[RES + '/drawable/bg_chip.xml'] = shape('#16FFFFFF', '20dp')
F[RES + '/drawable/bg_chip_on.xml'] = shape('#FFFFFF', '20dp')

# ---------- INFO DE LOS WIDGETS ----------
F[RES + '/xml/widget_grande_info.xml'] = '''<?xml version="1.0" encoding="utf-8"?>
<appwidget-provider xmlns:android="http://schemas.android.com/apk/res/android"
    android:minWidth="250dp"
    android:minHeight="180dp"
    android:targetCellWidth="4"
    android:targetCellHeight="3"
    android:updatePeriodMillis="1800000"
    android:initialLayout="@layout/widget_grande"
    android:resizeMode="horizontal|vertical"
    android:widgetCategory="home_screen"/>
'''
F[RES + '/xml/widget_chico_info.xml'] = '''<?xml version="1.0" encoding="utf-8"?>
<appwidget-provider xmlns:android="http://schemas.android.com/apk/res/android"
    android:minWidth="110dp"
    android:minHeight="110dp"
    android:targetCellWidth="2"
    android:targetCellHeight="2"
    android:updatePeriodMillis="1800000"
    android:initialLayout="@layout/widget_chico"
    android:resizeMode="horizontal|vertical"
    android:widgetCategory="home_screen"/>
'''

# ---------- LAYOUT GRANDE ----------
def tecla(idn, txt, orange=False):
    return '''      <TextView android:id="@+id/%s" android:layout_width="0dp" android:layout_height="match_parent" android:layout_weight="1" android:layout_margin="2dp"
          android:background="@drawable/%s" android:gravity="center" android:text="%s" android:textColor="%s" android:textSize="14sp" android:textStyle="bold"/>
''' % (idn, 'bg_key_o' if orange else 'bg_key', txt, '#FF8A4C' if orange else '#FFFFFF')

fila1 = ''.join(tecla('k%d' % n, str(n)) for n in (1, 2, 3, 4, 5)) + tecla('k_del', '&#x232B;', True)
fila2 = ''.join(tecla('k%d' % n, str(n)) for n in (6, 7, 8, 9, 0)) + tecla('k_punto', '.', True)

F[RES + '/layout/widget_grande.xml'] = '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/g_root" android:layout_width="match_parent" android:layout_height="match_parent"
    android:orientation="vertical" android:padding="12dp" android:background="@drawable/bg_widget">

  <RelativeLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginBottom="8dp">
    <TextView android:id="@+id/g_titulo" android:layout_width="wrap_content" android:layout_height="wrap_content"
        android:textColor="#FFFFFF" android:textSize="12sp" android:textStyle="bold"/>
    <TextView android:id="@+id/g_hace" android:layout_width="wrap_content" android:layout_height="wrap_content"
        android:layout_alignParentRight="true" android:textColor="#A5A8B0" android:textSize="10sp"/>
  </RelativeLayout>

  <LinearLayout android:layout_width="match_parent" android:layout_height="48dp" android:gravity="center_vertical" android:orientation="horizontal">
    <LinearLayout android:id="@+id/g_caja" android:layout_width="0dp" android:layout_height="match_parent" android:layout_weight="1.1"
        android:orientation="vertical" android:gravity="center_vertical" android:paddingLeft="10dp" android:paddingRight="6dp" android:background="@drawable/bg_orange">
      <TextView android:id="@+id/g_lbl_de" android:layout_width="wrap_content" android:layout_height="wrap_content" android:textColor="#E6FFFFFF" android:textSize="10sp"/>
      <TextView android:id="@+id/g_monto" android:layout_width="wrap_content" android:layout_height="wrap_content" android:maxLines="1" android:textColor="#FFFFFF" android:textSize="22sp" android:textStyle="bold"/>
    </LinearLayout>
    <TextView android:id="@+id/g_swap" android:layout_width="32dp" android:layout_height="32dp" android:layout_marginLeft="6dp" android:layout_marginRight="6dp"
        android:background="@drawable/bg_swap" android:gravity="center" android:textColor="#FFFFFF" android:textSize="16sp" android:textStyle="bold"/>
    <TextView android:id="@+id/g_pill" android:layout_width="0dp" android:layout_height="36dp" android:layout_weight="0.9"
        android:background="@drawable/bg_pill" android:gravity="center" android:textColor="#FFFFFF" android:textSize="13sp" android:textStyle="bold"/>
  </LinearLayout>

  <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="8dp" android:orientation="horizontal" android:gravity="bottom">
    <TextView android:id="@+id/g_res" android:layout_width="wrap_content" android:layout_height="wrap_content" android:maxLines="1" android:textColor="#FFFFFF" android:textSize="28sp" android:textStyle="bold"/>
    <TextView android:id="@+id/g_unidad" android:layout_width="wrap_content" android:layout_height="wrap_content" android:layout_marginLeft="4dp" android:layout_marginBottom="4dp" android:textColor="#A5A8B0" android:textSize="12sp" android:textStyle="bold"/>
    <FrameLayout android:layout_width="0dp" android:layout_height="1dp" android:layout_weight="1"/>
    <LinearLayout android:layout_width="wrap_content" android:layout_height="wrap_content" android:orientation="vertical" android:gravity="right">
      <TextView android:id="@+id/g_tasa" android:layout_width="wrap_content" android:layout_height="wrap_content" android:textColor="#A5A8B0" android:textSize="10sp"/>
      <TextView android:id="@+id/g_var" android:layout_width="wrap_content" android:layout_height="wrap_content" android:textSize="11sp" android:textStyle="bold"/>
    </LinearLayout>
  </LinearLayout>

  <LinearLayout android:layout_width="match_parent" android:layout_height="0dp" android:layout_weight="1" android:layout_marginTop="6dp" android:orientation="vertical">
    <LinearLayout android:layout_width="match_parent" android:layout_height="0dp" android:layout_weight="1" android:orientation="horizontal">
''' + fila1 + '''    </LinearLayout>
    <LinearLayout android:layout_width="match_parent" android:layout_height="0dp" android:layout_weight="1" android:orientation="horizontal">
''' + fila2 + '''    </LinearLayout>
  </LinearLayout>
</LinearLayout>
'''

# ---------- LAYOUT CHICO ----------
def chip(idn, txt):
    return '''    <TextView android:id="@+id/%s" android:layout_width="wrap_content" android:layout_height="22dp" android:layout_marginRight="5dp"
        android:background="@drawable/bg_chip" android:gravity="center" android:paddingLeft="9dp" android:paddingRight="9dp" android:text="%s" android:textColor="#FFFFFF" android:textSize="11sp" android:textStyle="bold"/>
''' % (idn, txt)

F[RES + '/layout/widget_chico.xml'] = '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/c_root" android:layout_width="match_parent" android:layout_height="match_parent"
    android:orientation="vertical" android:padding="12dp" android:background="@drawable/bg_widget">
  <TextView android:id="@+id/c_titulo" android:layout_width="wrap_content" android:layout_height="wrap_content" android:textColor="#FFFFFF" android:textSize="12sp" android:textStyle="bold"/>
  <FrameLayout android:layout_width="match_parent" android:layout_height="0dp" android:layout_weight="1"/>
  <TextView android:id="@+id/c_num" android:layout_width="wrap_content" android:layout_height="wrap_content" android:maxLines="1" android:textColor="#FFFFFF" android:textSize="24sp" android:textStyle="bold"/>
  <TextView android:id="@+id/c_sub" android:layout_width="wrap_content" android:layout_height="wrap_content" android:layout_marginTop="2dp" android:maxLines="1" android:textColor="#A5A8B0" android:textSize="10sp"/>
  <FrameLayout android:layout_width="match_parent" android:layout_height="0dp" android:layout_weight="1"/>
  <LinearLayout android:layout_width="wrap_content" android:layout_height="wrap_content" android:orientation="horizontal">
''' + chip('c_c1', '1') + chip('c_c2', '10') + chip('c_c3', '100') + '''  </LinearLayout>
</LinearLayout>
'''

# ---------- JAVA ----------
F[JD + '/WidgetDatos.java'] = r'''package __PKG__;

import android.content.Context;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.text.SpannableStringBuilder;
import android.text.Spanned;
import android.text.style.ForegroundColorSpan;
import android.text.style.RelativeSizeSpan;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.DecimalFormat;
import java.text.DecimalFormatSymbols;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class WidgetDatos {
    static final String[] MONEDAS = {"USD", "MXN", "EUR", "CAD", "GBP", "JPY", "BRL", "COP", "ARS"};
    static final String[][] PARES = {{"USD", "MXN"}, {"EUR", "MXN"}, {"GBP", "MXN"}, {"CAD", "MXN"}, {"MXN", "USD"}, {"USD", "EUR"}};

    static SharedPreferences sp(Context c) {
        return c.getApplicationContext().getSharedPreferences("widget_conv", Context.MODE_PRIVATE);
    }

    /** Descarga las tasas si tienen mas de 25 min (o si se fuerza). Llamar siempre fuera del hilo principal. */
    static synchronized void refrescar(Context c, boolean forzar) {
        SharedPreferences p = sp(c);
        long t = p.getLong("t", 0);
        if (!forzar && System.currentTimeMillis() - t < 25 * 60 * 1000L && p.getString("rates", null) != null) return;
        HttpURLConnection h = null;
        try {
            h = (HttpURLConnection) new URL("https://open.er-api.com/v6/latest/USD").openConnection();
            h.setConnectTimeout(8000);
            h.setReadTimeout(8000);
            BufferedReader r = new BufferedReader(new InputStreamReader(h.getInputStream(), "UTF-8"));
            StringBuilder sb = new StringBuilder();
            String ln;
            while ((ln = r.readLine()) != null) sb.append(ln);
            r.close();
            JSONObject rates = new JSONObject(sb.toString()).getJSONObject("rates");
            if (!rates.has("MXN")) return;
            String hoy = new SimpleDateFormat("yyyyMMdd", Locale.US).format(new Date());
            String dia = p.getString("dia", null);
            String viejo = p.getString("rates", null);
            SharedPreferences.Editor e = p.edit();
            if (dia != null && !dia.equals(hoy) && viejo != null) e.putString("base", viejo);
            e.putString("rates", rates.toString()).putString("dia", hoy).putLong("t", System.currentTimeMillis()).apply();
        } catch (Exception ex) {
            // sin conexion: se queda con lo guardado
        } finally {
            if (h != null) h.disconnect();
        }
    }

    static JSONObject json(Context c, String key) {
        try {
            String s = sp(c).getString(key, null);
            return s == null ? null : new JSONObject(s);
        } catch (Exception e) {
            return null;
        }
    }

    static double tasaDe(JSONObject r, String de, String a) {
        try {
            if (r == null || !r.has(de) || !r.has(a)) return Double.NaN;
            return r.getDouble(a) / r.getDouble(de);
        } catch (Exception e) {
            return Double.NaN;
        }
    }

    static double tasa(Context c, String de, String a) {
        return tasaDe(json(c, "rates"), de, a);
    }

    /** Cambio porcentual contra el ultimo dato del dia anterior. */
    static double variacion(Context c, String de, String a) {
        double n = tasaDe(json(c, "rates"), de, a);
        double b = tasaDe(json(c, "base"), de, a);
        if (Double.isNaN(n) || Double.isNaN(b) || b == 0) return Double.NaN;
        return (n / b - 1) * 100;
    }

    static String hace(Context c) {
        long t = sp(c).getLong("t", 0);
        if (t == 0) return "Sin datos";
        long m = (System.currentTimeMillis() - t) / 60000;
        if (m < 1) return "Actualizado ahora";
        if (m < 60) return "Actualizado hace " + m + " min";
        return "Actualizado hace " + (m / 60) + " h";
    }

    static DecimalFormat df(String pat) {
        return new DecimalFormat(pat, DecimalFormatSymbols.getInstance(Locale.US));
    }

    static double num(String s) {
        try {
            return Double.parseDouble(s);
        } catch (Exception e) {
            return 0;
        }
    }

    static String agrupar(String s) {
        int i = s.indexOf('.');
        String e = i < 0 ? s : s.substring(0, i);
        String d = i < 0 ? "" : s.substring(i);
        StringBuilder sb = new StringBuilder();
        int n = e.length();
        for (int k = 0; k < n; k++) {
            if (k > 0 && (n - k) % 3 == 0) sb.append(',');
            sb.append(e.charAt(k));
        }
        return sb.toString() + d;
    }

    static CharSequence resultado(double v) {
        if (Double.isNaN(v) || Double.isInfinite(v)) return "—";
        String s = df(Math.abs(v) < 1 ? "#,##0.0000" : "#,##0.00").format(v);
        int i = s.indexOf('.');
        SpannableStringBuilder b = new SpannableStringBuilder(s);
        if (i >= 0) {
            b.setSpan(new RelativeSizeSpan(0.6f), i, s.length(), Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
            b.setSpan(new ForegroundColorSpan(Color.parseColor("#9A9CA4")), i, s.length(), Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
        }
        return b;
    }

    static CharSequence varTxt(double v) {
        if (Double.isNaN(v)) return "";
        boolean up = v >= 0;
        String s = (up ? "▲ " : "▼ ") + df("0.0").format(Math.abs(v)) + " %";
        SpannableStringBuilder b = new SpannableStringBuilder(s);
        b.setSpan(new ForegroundColorSpan(Color.parseColor(up ? "#3DDC97" : "#FF6B6B")), 0, s.length(), Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
        return b;
    }

    static CharSequence titulo(String t) {
        String s = "●  " + t;
        SpannableStringBuilder b = new SpannableStringBuilder(s);
        b.setSpan(new ForegroundColorSpan(Color.parseColor("#FF6A2B")), 0, 1, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
        return b;
    }
}
'''

F[JD + '/ConvWidgetGrande.java'] = r'''package __PKG__;

import android.app.PendingIntent;
import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.widget.RemoteViews;

public class ConvWidgetGrande extends AppWidgetProvider {
    static final String ACC = "__PKG__.ACC_GRANDE";

    @Override
    public void onUpdate(final Context c, final AppWidgetManager m, final int[] ids) {
        for (int id : ids) pintar(c, m, id);
        final PendingResult pr = goAsync();
        new Thread(new Runnable() {
            public void run() {
                try {
                    WidgetDatos.refrescar(c, false);
                    for (int id : ids) pintar(c, m, id);
                } catch (Exception e) {
                }
                pr.finish();
            }
        }).start();
    }

    @Override
    public void onReceive(final Context c, final Intent i) {
        if (ACC.equals(i.getAction())) {
            final String k = i.getStringExtra("k");
            final PendingResult pr = goAsync();
            new Thread(new Runnable() {
                public void run() {
                    try {
                        tecla(c, k);
                        repintar(c);
                        WidgetDatos.refrescar(c, false);
                        repintar(c);
                    } catch (Exception e) {
                    }
                    pr.finish();
                }
            }).start();
        } else {
            super.onReceive(c, i);
        }
    }

    static void repintar(Context c) {
        AppWidgetManager m = AppWidgetManager.getInstance(c);
        int[] ids = m.getAppWidgetIds(new ComponentName(c, ConvWidgetGrande.class));
        for (int id : ids) pintar(c, m, id);
    }

    static void tecla(Context c, String k) {
        if (k == null) return;
        SharedPreferences p = WidgetDatos.sp(c);
        String mo = p.getString("g_monto", "100");
        boolean ini = p.getBoolean("g_ini", true);
        int de = p.getInt("g_de", 0);
        int a = p.getInt("g_a", 1);
        int n = WidgetDatos.MONEDAS.length;
        if (k.equals("d")) {
            mo = mo.length() <= 1 ? "0" : mo.substring(0, mo.length() - 1);
            ini = false;
        } else if (k.equals(".")) {
            if (ini) mo = "0.";
            else if (mo.indexOf('.') < 0) mo += ".";
            ini = false;
        } else if (k.equals("s")) {
            int t = de;
            de = a;
            a = t;
        } else if (k.equals("de")) {
            de = (de + 1) % n;
            if (de == a) de = (de + 1) % n;
        } else if (k.equals("a")) {
            a = (a + 1) % n;
            if (a == de) a = (a + 1) % n;
        } else if (k.length() == 1 && Character.isDigit(k.charAt(0))) {
            int pt = mo.indexOf('.');
            if (ini || mo.equals("0")) mo = k;
            else if (mo.length() < 12 && (pt < 0 || mo.length() - pt <= 4)) mo += k;
            ini = false;
        }
        p.edit().putString("g_monto", mo).putBoolean("g_ini", ini).putInt("g_de", de).putInt("g_a", a).apply();
    }

    static PendingIntent pi(Context c, String k, int rc) {
        Intent i = new Intent(c, ConvWidgetGrande.class);
        i.setAction(ACC);
        i.putExtra("k", k);
        i.setData(Uri.parse("conv://grande/" + k));
        return PendingIntent.getBroadcast(c, rc, i, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
    }

    static PendingIntent abrir(Context c) {
        Intent i = c.getPackageManager().getLaunchIntentForPackage(c.getPackageName());
        return PendingIntent.getActivity(c, 1, i, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
    }

    static void pintar(Context c, AppWidgetManager m, int id) {
        SharedPreferences p = WidgetDatos.sp(c);
        String mo = p.getString("g_monto", "100");
        int de = p.getInt("g_de", 0);
        int a = p.getInt("g_a", 1);
        String D = WidgetDatos.MONEDAS[de];
        String A = WidgetDatos.MONEDAS[a];
        RemoteViews v = new RemoteViews(c.getPackageName(), R.layout.widget_grande);
        v.setTextViewText(R.id.g_titulo, WidgetDatos.titulo("Convertidor"));
        v.setTextViewText(R.id.g_hace, WidgetDatos.hace(c));
        v.setTextViewText(R.id.g_lbl_de, "Tengo · " + D);
        v.setTextViewText(R.id.g_monto, WidgetDatos.agrupar(mo));
        v.setTextViewText(R.id.g_swap, "⇄");
        v.setTextViewText(R.id.g_pill, A + " ▾");
        double t = WidgetDatos.tasa(c, D, A);
        v.setTextViewText(R.id.g_res, WidgetDatos.resultado(WidgetDatos.num(mo) * t));
        v.setTextViewText(R.id.g_unidad, A);
        v.setTextViewText(R.id.g_tasa, Double.isNaN(t) ? "" : "1 " + D + " = " + WidgetDatos.df(t < 1 ? "0.0000" : "0.00").format(t));
        v.setTextViewText(R.id.g_var, WidgetDatos.varTxt(WidgetDatos.variacion(c, D, A)));

        v.setOnClickPendingIntent(R.id.g_titulo, abrir(c));
        v.setOnClickPendingIntent(R.id.g_caja, pi(c, "de", 200));
        v.setOnClickPendingIntent(R.id.g_swap, pi(c, "s", 201));
        v.setOnClickPendingIntent(R.id.g_pill, pi(c, "a", 202));
        int[] ids = {R.id.k0, R.id.k1, R.id.k2, R.id.k3, R.id.k4, R.id.k5, R.id.k6, R.id.k7, R.id.k8, R.id.k9, R.id.k_punto, R.id.k_del};
        String[] ks = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "d"};
        for (int j = 0; j < ids.length; j++) v.setOnClickPendingIntent(ids[j], pi(c, ks[j], 100 + j));
        m.updateAppWidget(id, v);
    }
}
'''

F[JD + '/ConvWidgetChico.java'] = r'''package __PKG__;

import android.app.PendingIntent;
import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.text.SpannableStringBuilder;
import android.widget.RemoteViews;

public class ConvWidgetChico extends AppWidgetProvider {
    static final String ACC = "__PKG__.ACC_CHICO";
    static final int[] MONTOS = {1, 10, 100};

    @Override
    public void onUpdate(final Context c, final AppWidgetManager m, final int[] ids) {
        for (int id : ids) pintar(c, m, id);
        final PendingResult pr = goAsync();
        new Thread(new Runnable() {
            public void run() {
                try {
                    WidgetDatos.refrescar(c, false);
                    for (int id : ids) pintar(c, m, id);
                } catch (Exception e) {
                }
                pr.finish();
            }
        }).start();
    }

    @Override
    public void onDeleted(Context c, int[] ids) {
        SharedPreferences.Editor e = WidgetDatos.sp(c).edit();
        for (int id : ids) e.remove("c_par_" + id).remove("c_mon_" + id);
        e.apply();
    }

    @Override
    public void onReceive(final Context c, final Intent i) {
        if (ACC.equals(i.getAction())) {
            final int id = i.getIntExtra("id", 0);
            final String k = i.getStringExtra("k");
            final PendingResult pr = goAsync();
            new Thread(new Runnable() {
                public void run() {
                    try {
                        SharedPreferences p = WidgetDatos.sp(c);
                        if ("par".equals(k)) {
                            p.edit().putInt("c_par_" + id, (p.getInt("c_par_" + id, 0) + 1) % WidgetDatos.PARES.length).apply();
                        } else if (k != null) {
                            p.edit().putInt("c_mon_" + id, Integer.parseInt(k)).apply();
                        }
                        repintar(c);
                        WidgetDatos.refrescar(c, false);
                        repintar(c);
                    } catch (Exception e) {
                    }
                    pr.finish();
                }
            }).start();
        } else {
            super.onReceive(c, i);
        }
    }

    static void repintar(Context c) {
        AppWidgetManager m = AppWidgetManager.getInstance(c);
        int[] ids = m.getAppWidgetIds(new ComponentName(c, ConvWidgetChico.class));
        for (int id : ids) pintar(c, m, id);
    }

    static PendingIntent pi(Context c, int id, String k) {
        Intent i = new Intent(c, ConvWidgetChico.class);
        i.setAction(ACC);
        i.putExtra("id", id);
        i.putExtra("k", k);
        i.setData(Uri.parse("conv://chico/" + id + "/" + k));
        return PendingIntent.getBroadcast(c, id * 10 + k.hashCode() % 7, i, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
    }

    static void pintar(Context c, AppWidgetManager m, int id) {
        SharedPreferences p = WidgetDatos.sp(c);
        int par = p.getInt("c_par_" + id, 0) % WidgetDatos.PARES.length;
        int mon = p.getInt("c_mon_" + id, 1);
        String D = WidgetDatos.PARES[par][0];
        String A = WidgetDatos.PARES[par][1];
        double t = WidgetDatos.tasa(c, D, A);
        RemoteViews v = new RemoteViews(c.getPackageName(), R.layout.widget_chico);
        v.setTextViewText(R.id.c_titulo, WidgetDatos.titulo(D + " → " + A));
        v.setTextViewText(R.id.c_num, WidgetDatos.resultado(mon * t));
        SpannableStringBuilder sub = new SpannableStringBuilder(mon + " " + D + "   ");
        sub.append(WidgetDatos.varTxt(WidgetDatos.variacion(c, D, A)));
        v.setTextViewText(R.id.c_sub, sub);
        v.setOnClickPendingIntent(R.id.c_titulo, pi(c, id, "par"));
        int[] chips = {R.id.c_c1, R.id.c_c2, R.id.c_c3};
        for (int j = 0; j < 3; j++) {
            boolean on = MONTOS[j] == mon;
            v.setInt(chips[j], "setBackgroundResource", on ? R.drawable.bg_chip_on : R.drawable.bg_chip);
            v.setTextColor(chips[j], on ? 0xFF111111 : 0xFFFFFFFF);
            v.setOnClickPendingIntent(chips[j], pi(c, id, String.valueOf(MONTOS[j])));
        }
        m.updateAppWidget(id, v);
    }
}
'''

# ---------- ESCRIBIR ARCHIVOS ----------
if not os.path.isdir(JD):
    sys.exit('No encuentro la carpeta de Java: ' + JD)
for path, content in F.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.replace('__PKG__', PKG))

# ---------- REGISTRAR EN EL MANIFEST ----------
mf = os.path.join(BASE, 'AndroidManifest.xml')
s = open(mf, encoding='utf-8').read()
if 'ConvWidgetGrande' not in s:
    rec = ''
    for clase, nombre, info in (('ConvWidgetGrande', 'Convertidor 4x3', 'widget_grande_info'), ('ConvWidgetChico', 'Tipo de cambio 2x2', 'widget_chico_info')):
        rec += '''
        <receiver android:name="%s.%s" android:exported="true" android:label="%s">
            <intent-filter><action android:name="android.appwidget.action.APPWIDGET_UPDATE"/></intent-filter>
            <meta-data android:name="android.appwidget.provider" android:resource="@xml/%s"/>
        </receiver>
''' % (PKG, clase, nombre, info)
    assert '</application>' in s
    s = s.replace('</application>', rec + '    </application>', 1)
    open(mf, 'w', encoding='utf-8').write(s)
print('Widgets agregados en', PKG)
