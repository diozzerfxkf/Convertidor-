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


# ---------- WIDGET DE MERCADOS (paleta vino / lila / durazno + grafica) ----------
F[RES + '/xml/widget_mercados_info.xml'] = """<?xml version="1.0" encoding="utf-8"?>
<appwidget-provider xmlns:android="http://schemas.android.com/apk/res/android"
    android:minWidth="250dp"
    android:minHeight="120dp"
    android:targetCellWidth="4"
    android:targetCellHeight="2"
    android:updatePeriodMillis="1800000"
    android:initialLayout="@layout/widget_mercados"
    android:configure="__PKG__.ConfigMercados"
    android:widgetFeatures="reconfigurable"
    android:resizeMode="horizontal|vertical"
    android:widgetCategory="home_screen"/>
"""

F[RES + '/layout/widget_mercados.xml'] = """<?xml version="1.0" encoding="utf-8"?>
<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/m_root" android:layout_width="match_parent" android:layout_height="match_parent">
  <ImageView android:id="@+id/m_img" android:layout_width="match_parent" android:layout_height="match_parent" android:scaleType="fitCenter"/>
  <FrameLayout android:id="@+id/m_z_todo" android:layout_width="match_parent" android:layout_height="match_parent"/>
</FrameLayout>
"""

F[JD + '/MercadoDatos.java'] = r"""package __PKG__;

import android.content.Context;
import android.content.SharedPreferences;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.Iterator;
import java.util.Locale;
import java.util.TimeZone;
import java.util.TreeMap;

public class MercadoDatos {
    static final String[] COD = {"SYD", "TYO", "LON", "NYC"};
    static final String[] NOM = {"Sídney", "Tokio", "Londres", "Nueva York"};
    static final String[] TZ = {"Australia/Sydney", "Asia/Tokyo", "Europe/London", "America/New_York"};
    // hora de apertura y cierre (hora local de cada bolsa): {h, min, h, min}
    static final int[][] HORA = {{10, 0, 16, 0}, {9, 0, 15, 30}, {8, 0, 16, 30}, {9, 30, 16, 0}};

    static final String[] MONEDAS = {"USD", "EUR", "GBP", "JPY", "CAD", "MXN", "BRL", "AUD", "CHF", "CNY"};
    static final int[] DIAS = {30, 90, 180};
    static final String[] DIAS_TXT = {"1M", "3M", "6M"};
    static final int[] AGRUPA = {2, 3, 5};

    static final String[] ZONAS_ID = {"", "America/Mexico_City", "America/New_York", "Europe/London", "Asia/Tokyo", "UTC"};
    static final String[] ZONAS_ET = {"hora local", "CDMX", "Nueva York", "Londres", "Tokio", "UTC"};

    static class Estado {
        int idx;
        boolean abierto;
        long objetivo;
    }

    static Calendar cal(int i, long ahora, int dia) {
        Calendar x = Calendar.getInstance(TimeZone.getTimeZone(TZ[i]));
        x.setTimeInMillis(ahora);
        x.add(Calendar.DAY_OF_YEAR, dia);
        return x;
    }

    static boolean habil(int i, long ahora, int dia) {
        int d = cal(i, ahora, dia).get(Calendar.DAY_OF_WEEK);
        return d != Calendar.SATURDAY && d != Calendar.SUNDAY;
    }

    static long ms(int i, long ahora, int dia, int h, int mi) {
        Calendar x = cal(i, ahora, dia);
        x.set(Calendar.HOUR_OF_DAY, h);
        x.set(Calendar.MINUTE, mi);
        x.set(Calendar.SECOND, 0);
        x.set(Calendar.MILLISECOND, 0);
        return x.getTimeInMillis();
    }

    static Estado estado(int i, long ahora) {
        Estado e = new Estado();
        e.idx = i;
        if (habil(i, ahora, 0)) {
            long a = ms(i, ahora, 0, HORA[i][0], HORA[i][1]);
            long z = ms(i, ahora, 0, HORA[i][2], HORA[i][3]);
            if (ahora >= a && ahora < z) {
                e.abierto = true;
                e.objetivo = z;
                return e;
            }
        }
        for (int d = 0; d <= 8; d++) {
            if (habil(i, ahora, d)) {
                long a = ms(i, ahora, d, HORA[i][0], HORA[i][1]);
                if (a > ahora) {
                    e.objetivo = a;
                    return e;
                }
            }
        }
        e.objetivo = ahora;
        return e;
    }

    /** El mercado que abre primero entre los que estan cerrados. */
    static Estado auto(long ahora) {
        Estado mejor = null;
        for (int i = 0; i < COD.length; i++) {
            Estado e = estado(i, ahora);
            if (!e.abierto && (mejor == null || e.objetivo < mejor.objetivo)) mejor = e;
        }
        return mejor != null ? mejor : estado(0, ahora);
    }

    /** Hora de apertura/cierre en la zona y formato (12 o 24 h) que eligio la persona. */
    static String horaTxt(Context c, long t) {
        SharedPreferences pr = WidgetDatos.sp(c);
        int z = pr.getInt("m_zona", 0);
        if (z < 0 || z >= ZONAS_ID.length) z = 0;
        boolean h12 = pr.getInt("m_f", 0) == 1;
        TimeZone tz = z == 0 ? TimeZone.getDefault() : TimeZone.getTimeZone(ZONAS_ID[z]);
        SimpleDateFormat hf = new SimpleDateFormat(h12 ? "h:mm a" : "HH:mm", Locale.US);
        hf.setTimeZone(tz);
        SimpleDateFormat df = new SimpleDateFormat("yyyyMMdd", Locale.US);
        df.setTimeZone(tz);
        SimpleDateFormat dn = new SimpleDateFormat("EEE", new Locale("es", "MX"));
        dn.setTimeZone(tz);
        Date d = new Date(t);
        String dia = df.format(d).equals(df.format(new Date())) ? "" : dn.format(d) + " ";
        return dia + hf.format(d) + " · " + ZONAS_ET[z];
    }

    static class Serie {
        String[] f = new String[0];
        double[] v = new double[0];
    }

    static String clave(String de, String a, int dias) {
        return "hs_" + de + a + dias;
    }

    static Serie serie(Context c, String de, String a, int dias) {
        Serie s = new Serie();
        String txt = WidgetDatos.sp(c).getString(clave(de, a, dias), null);
        if (txt == null || txt.length() == 0) return s;
        String[] partes = txt.split(";");
        String[] f = new String[partes.length];
        double[] v = new double[partes.length];
        int n = 0;
        for (String p : partes) {
            int k = p.indexOf('=');
            if (k < 0) continue;
            try {
                f[n] = p.substring(0, k);
                v[n] = Double.parseDouble(p.substring(k + 1));
                n++;
            } catch (Exception e) {
            }
        }
        s.f = new String[n];
        s.v = new double[n];
        System.arraycopy(f, 0, s.f, 0, n);
        System.arraycopy(v, 0, s.v, 0, n);
        return s;
    }

    /** Baja la grafica del par y rango elegidos si tiene mas de 3 horas. Llamar fuera del hilo principal. */
    static synchronized void refrescar(Context c, boolean forzar) {
        SharedPreferences p = WidgetDatos.sp(c);
        String de = p.getString("m_de", "USD");
        String a = p.getString("m_a", "MXN");
        int rg = p.getInt("m_rango", 0) % DIAS.length;
        if (de.equals(a)) return;
        int dias = DIAS[rg];
        String k = clave(de, a, dias);
        long t = p.getLong(k + "_t", 0);
        if (!forzar && System.currentTimeMillis() - t < 3 * 60 * 60 * 1000L && p.getString(k, null) != null) return;
        HttpURLConnection h = null;
        try {
            SimpleDateFormat sf = new SimpleDateFormat("yyyy-MM-dd", Locale.US);
            Calendar x = Calendar.getInstance();
            x.add(Calendar.DAY_OF_YEAR, -dias);
            String url = "https://api.frankfurter.dev/v1/" + sf.format(x.getTime()) + "..?base=" + de + "&symbols=" + a;
            h = (HttpURLConnection) new URL(url).openConnection();
            h.setConnectTimeout(8000);
            h.setReadTimeout(10000);
            BufferedReader r = new BufferedReader(new InputStreamReader(h.getInputStream(), "UTF-8"));
            StringBuilder sb = new StringBuilder();
            String ln;
            while ((ln = r.readLine()) != null) sb.append(ln);
            r.close();
            JSONObject rates = new JSONObject(sb.toString()).getJSONObject("rates");
            TreeMap<String, Double> orden = new TreeMap<String, Double>();
            Iterator<String> it = rates.keys();
            while (it.hasNext()) {
                String d = it.next();
                orden.put(d, rates.getJSONObject(d).getDouble(a));
            }
            if (orden.size() < 2) return;
            StringBuilder out = new StringBuilder();
            for (java.util.Map.Entry<String, Double> en : orden.entrySet()) {
                if (out.length() > 0) out.append(';');
                out.append(en.getKey()).append('=').append(en.getValue());
            }
            p.edit().putString(k, out.toString()).putLong(k + "_t", System.currentTimeMillis()).apply();
        } catch (Exception ex) {
            // sin conexion: se queda con lo guardado
        } finally {
            if (h != null) h.disconnect();
        }
    }
}
"""

F[JD + '/ConvWidgetMercados.java'] = r"""package __PKG__;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.LinearGradient;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.RadialGradient;
import android.graphics.RectF;
import android.graphics.Shader;
import android.graphics.Typeface;
import android.net.Uri;
import android.os.SystemClock;
import android.widget.RemoteViews;

public class ConvWidgetMercados extends AppWidgetProvider {
    static final String ACC = "__PKG__.ACC_MERCADOS";
    static final int W = 960;
    static final int H = 480;
    // paleta: Crimson Violet, Clouded Periwinkle, Apricot Silk
    static final int CRIM = 0xFF470B24;
    static final int PERI = 0xFFB5BEDD;
    static final int APRI = 0xFFFFEDD5;
    static final int MUTE = 0xFF6B4A5E;
    static final int SUBE = 0xFF1F7A5C;
    static final int BAJA = 0xFFA8122E;
    static final int ACENTO = 0xFFC2185B;
    static final String[] MESES = {"ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"};

    // letras de puntos 5x7
    static final String[][] GLIFOS = {
        {"01110", "10001", "10011", "10101", "11001", "10001", "01110"},
        {"00100", "01100", "00100", "00100", "00100", "00100", "01110"},
        {"01110", "10001", "00001", "00010", "00100", "01000", "11111"},
        {"11110", "00001", "00001", "01110", "00001", "00001", "11110"},
        {"00010", "00110", "01010", "10010", "11111", "00010", "00010"},
        {"11111", "10000", "11110", "00001", "00001", "10001", "01110"},
        {"00110", "01000", "10000", "11110", "10001", "10001", "01110"},
        {"11111", "00001", "00010", "00100", "01000", "01000", "01000"},
        {"01110", "10001", "10001", "01110", "10001", "10001", "01110"},
        {"01110", "10001", "10001", "01111", "00001", "00010", "01100"}
    };

    @Override
    public void onEnabled(Context c) {
        programar(c);
    }

    @Override
    public void onDisabled(Context c) {
        AlarmManager am = (AlarmManager) c.getSystemService(Context.ALARM_SERVICE);
        if (am != null) am.cancel(pi(c, "tick", 300));
    }

    @Override
    public void onUpdate(final Context c, final AppWidgetManager m, final int[] ids) {
        repintar(c);
        programar(c);
        final PendingResult pr = goAsync();
        new Thread(new Runnable() {
            public void run() {
                try {
                    WidgetDatos.refrescar(c, false);
                    MercadoDatos.refrescar(c, false);
                    repintar(c);
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
                        repintar(c);
                        MercadoDatos.refrescar(c, false);
                        repintar(c);
                        if ("tick".equals(k)) programar(c);
                    } catch (Exception e) {
                    }
                    pr.finish();
                }
            }).start();
        } else {
            super.onReceive(c, i);
        }
    }

    /** Un aviso cada minuto mientras haya widgets (no despierta el telefono). */
    static void programar(Context c) {
        AlarmManager am = (AlarmManager) c.getSystemService(Context.ALARM_SERVICE);
        if (am == null) return;
        int[] ids = AppWidgetManager.getInstance(c).getAppWidgetIds(new ComponentName(c, ConvWidgetMercados.class));
        if (ids.length == 0) return;
        am.set(AlarmManager.ELAPSED_REALTIME, SystemClock.elapsedRealtime() + 60000L, pi(c, "tick", 300));
    }

    static PendingIntent pi(Context c, String k, int rc) {
        Intent i = new Intent(c, ConvWidgetMercados.class);
        i.setAction(ACC);
        i.putExtra("k", k);
        i.setData(Uri.parse("conv://mercados/" + k));
        return PendingIntent.getBroadcast(c, rc, i, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
    }

    static PendingIntent config(Context c) {
        Intent i = new Intent(c, ConfigMercados.class);
        i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        return PendingIntent.getActivity(c, 5, i, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
    }

    static void repintar(Context c) {
        AppWidgetManager m = AppWidgetManager.getInstance(c);
        int[] ids = m.getAppWidgetIds(new ComponentName(c, ConvWidgetMercados.class));
        if (ids.length == 0) return;
        Bitmap b = dibujar(c);
        for (int id : ids) {
            RemoteViews v = new RemoteViews(c.getPackageName(), R.layout.widget_mercados);
            v.setImageViewBitmap(R.id.m_img, b);
            v.setOnClickPendingIntent(R.id.m_z_todo, config(c));
            m.updateAppWidget(id, v);
        }
    }

    static String dos(long n) {
        return n < 10 ? "0" + n : String.valueOf(n);
    }

    static String fmtEje(double v) {
        if (v >= 100) return WidgetDatos.df("0").format(v);
        if (v >= 10) return WidgetDatos.df("0.0").format(v);
        if (v >= 1) return WidgetDatos.df("0.00").format(v);
        return WidgetDatos.df("0.000").format(v);
    }

    static String fecha(String iso) {
        try {
            int mes = Integer.parseInt(iso.substring(5, 7)) - 1;
            return Integer.parseInt(iso.substring(8, 10)) + " " + MESES[mes];
        } catch (Exception e) {
            return iso;
        }
    }

    static float anchoPuntos(String s, float d) {
        float w = 0;
        for (int i = 0; i < s.length(); i++) {
            w += (s.charAt(i) == ':' ? 1 : 5) * d + d;
        }
        return w - d;
    }

    static void puntos(Canvas cv, Paint p, String s, float xDer, float yTop, float d, float r) {
        float x = xDer - anchoPuntos(s, d);
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == ':') {
                p.setColor(PERI);
                cv.drawCircle(x + r, yTop + 2 * d + r, r, p);
                cv.drawCircle(x + r, yTop + 4 * d + r, r, p);
                x += d + d;
            } else if (ch >= '0' && ch <= '9') {
                p.setColor(APRI);
                String[] g = GLIFOS[ch - '0'];
                for (int fila = 0; fila < 7; fila++) {
                    for (int col = 0; col < 5; col++) {
                        if (g[fila].charAt(col) == '1') cv.drawCircle(x + col * d + r, yTop + fila * d + r, r, p);
                    }
                }
                x += 5 * d + d;
            }
        }
    }

    static float yDe(double v, double mn, double mx, float y0, float y1) {
        return (float) (y1 - (v - mn) / (mx - mn) * (y1 - y0));
    }

    static void fondo(Canvas cv, Paint p) {
        // borde inferior (efecto de tarjeta apilada)
        p.setStyle(Paint.Style.FILL);
        p.setColor(0xFFE2C29B);
        cv.drawRoundRect(new RectF(0, 10, W, H), 56, 56, p);
        RectF tarjeta = new RectF(0, 0, W, H - 10);
        p.setShader(new LinearGradient(W * 0.52f, 0, W * 0.48f, H - 10,
            new int[]{CRIM, CRIM, PERI, PERI, APRI}, new float[]{0f, 0.33f, 0.45f, 0.60f, 1f}, Shader.TileMode.CLAMP));
        cv.drawRoundRect(tarjeta, 56, 56, p);
        p.setShader(null);
        // manchas de color suaves
        Path recorte = new Path();
        recorte.addRoundRect(tarjeta, 56, 56, Path.Direction.CW);
        cv.save();
        cv.clipPath(recorte);
        p.setShader(new RadialGradient(W * 0.08f, H * 0.62f, 260, new int[]{0xB8B5BEDD, 0x00B5BEDD}, null, Shader.TileMode.CLAMP));
        cv.drawRect(0, 0, W, H, p);
        p.setShader(new RadialGradient(W * 0.88f, 0, 230, new int[]{0xFF470B24, 0x00470B24}, null, Shader.TileMode.CLAMP));
        cv.drawRect(0, 0, W, H, p);
        p.setShader(new RadialGradient(W * 0.55f, H, 460, new int[]{0xFFFFEDD5, 0x00FFEDD5}, null, Shader.TileMode.CLAMP));
        cv.drawRect(0, 0, W, H, p);
        p.setShader(null);
        cv.restore();
    }

    static Bitmap dibujar(Context c) {
        Bitmap bm = Bitmap.createBitmap(W, H, Bitmap.Config.ARGB_8888);
        Canvas cv = new Canvas(bm);
        Paint p = new Paint(Paint.ANTI_ALIAS_FLAG);
        SharedPreferences pr = WidgetDatos.sp(c);
        long ahora = System.currentTimeMillis();
        fondo(cv, p);

        // mercado elegido
        int sel = pr.getInt("m_sel", 0);
        if (sel < 0 || sel > MercadoDatos.COD.length) sel = 0;
        MercadoDatos.Estado e = sel == 0 ? MercadoDatos.auto(ahora) : MercadoDatos.estado(sel - 1, ahora);
        long mins = (e.objetivo - ahora + 59999L) / 60000L;
        if (mins < 0) mins = 0;
        long hh = mins / 60;
        if (hh > 99) hh = 99;
        String cuenta = dos(hh) + ":" + dos(mins % 60);

        // titulo, mercado y hora
        p.setStyle(Paint.Style.FILL);
        p.setTextAlign(Paint.Align.LEFT);
        p.setTypeface(Typeface.create("sans-serif-light", Typeface.NORMAL));
        p.setColor(APRI);
        p.setTextSize(62);
        cv.drawText("Mercados", 40, 84, p);
        p.setTypeface(Typeface.create("sans-serif", Typeface.NORMAL));
        p.setColor(PERI);
        p.setTextSize(28);
        cv.drawText(MercadoDatos.NOM[e.idx] + (e.abierto ? " cierra en" : " abre en"), 40, 122, p);
        p.setTextSize(22);
        cv.drawText((e.abierto ? "Cierra " : "Abre ") + MercadoDatos.horaTxt(c, e.objetivo), 40, 152, p);

        // cuenta regresiva de puntos
        puntos(cv, p, cuenta, 806, 32, 15, 5.8f);

        // insignia del mercado
        p.setColor(0x33FFEDD5);
        cv.drawRoundRect(new RectF(836, 34, 922, 150), 24, 24, p);
        p.setColor(e.abierto ? 0xFF5FE3A1 : 0xFF8A7A8F);
        cv.drawCircle(879, 62, 8, p);
        p.setColor(APRI);
        p.setTypeface(Typeface.create("sans-serif", Typeface.BOLD));
        p.setTextAlign(Paint.Align.CENTER);
        p.setTextSize(28);
        cv.drawText(MercadoDatos.COD[e.idx], 879, 108, p);
        p.setTypeface(Typeface.create("sans-serif", Typeface.NORMAL));
        p.setTextSize(15);
        p.setColor(PERI);
        cv.drawText(e.abierto ? "ABIERTO" : "CERRADO", 879, 134, p);

        // grafica de la divisa elegida
        String de = pr.getString("m_de", "USD");
        String a = pr.getString("m_a", "MXN");
        int rg = pr.getInt("m_rango", 0) % MercadoDatos.DIAS.length;
        int tipo = pr.getInt("m_tipo", 0);
        MercadoDatos.Serie s = MercadoDatos.serie(c, de, a, MercadoDatos.DIAS[rg]);
        int n = s.v.length;

        p.setTextAlign(Paint.Align.LEFT);
        p.setTypeface(Typeface.create("sans-serif", Typeface.BOLD));
        p.setColor(CRIM);
        p.setTextSize(26);
        String etiqueta = de + "/" + a;
        cv.drawText(etiqueta, 40, 224, p);
        float xv = 40 + p.measureText(etiqueta) + 14;
        p.setTypeface(Typeface.create("sans-serif", Typeface.NORMAL));
        p.setTextSize(24);
        String rangoTxt = MercadoDatos.DIAS_TXT[rg];

        if (n < 2 || de.equals(a)) {
            p.setColor(MUTE);
            cv.drawText(rangoTxt, xv, 224, p);
            p.setTextAlign(Paint.Align.CENTER);
            p.setTextSize(28);
            cv.drawText(de.equals(a) ? "Elige dos divisas distintas" : "Sin datos de la gráfica (toca para configurar)", W / 2f, 300, p);
        } else {
            double ult = s.v[n - 1];
            double var = (ult / s.v[0] - 1) * 100;
            boolean sube = var >= 0;
            p.setColor(CRIM);
            p.setTextSize(26);
            cv.drawText(WidgetDatos.df(ult < 1 ? "0.0000" : "0.00").format(ult), xv, 224, p);
            p.setTextAlign(Paint.Align.RIGHT);
            p.setColor(sube ? SUBE : BAJA);
            cv.drawText((sube ? "▲ " : "▼ ") + WidgetDatos.df("0.0").format(Math.abs(var)) + " %  ·  " + rangoTxt, 922, 224, p);

            double mn = s.v[0], mx = s.v[0];
            for (int i = 1; i < n; i++) {
                if (s.v[i] < mn) mn = s.v[i];
                if (s.v[i] > mx) mx = s.v[i];
            }
            double pad = (mx - mn) * 0.1;
            if (pad == 0) pad = mx * 0.001;
            mn -= pad;
            mx += pad;
            final float x0 = 120, x1 = 918, y0 = 252, y1 = 342;

            // lineas guia y etiquetas del eje Y
            p.setTextAlign(Paint.Align.LEFT);
            p.setTextSize(21);
            double[] marcas = {mx - pad, (mx + mn) / 2, mn + pad};
            for (int k = 0; k < 3; k++) {
                float y = yDe(marcas[k], mn, mx, y0, y1);
                p.setColor(0x24470B24);
                cv.drawRect(x0 - 8, y - 1, x1 + 6, y + 1, p);
                p.setColor(MUTE);
                cv.drawText(fmtEje(marcas[k]), 40, y + 7, p);
            }

            float paso = (x1 - x0) / (n - 1);
            // puntitos en la base
            p.setColor(0x66470B24);
            for (int i = 0; i < n; i++) cv.drawCircle(x0 + i * paso, y1 + 18, 1.8f, p);

            p.setStrokeCap(Paint.Cap.ROUND);
            if (tipo == 0) {
                // velas japonesas (agrupando cierres diarios)
                int g = MercadoDatos.AGRUPA[rg];
                int m = (n - 1 + g - 1) / g;
                float ranura = (x1 - x0) / m;
                float cuerpo = Math.max(6f, Math.min(20f, ranura * 0.58f));
                for (int k = 0; k < m; k++) {
                    int ia = k * g;
                    int ib = Math.min(n - 1, (k + 1) * g);
                    double ap = s.v[ia], ci = s.v[ib], alto = ap, bajo = ap;
                    for (int j = ia; j <= ib; j++) {
                        if (s.v[j] > alto) alto = s.v[j];
                        if (s.v[j] < bajo) bajo = s.v[j];
                    }
                    float cx = x0 + (k + 0.5f) * ranura;
                    float yA = yDe(ap, mn, mx, y0, y1), yC = yDe(ci, mn, mx, y0, y1);
                    float yH = yDe(alto, mn, mx, y0, y1), yL = yDe(bajo, mn, mx, y0, y1);
                    int col = ci >= ap ? SUBE : BAJA;
                    p.setColor(col);
                    p.setStyle(Paint.Style.STROKE);
                    p.setStrokeWidth(3f);
                    cv.drawLine(cx, yH, cx, yL, p);
                    p.setStyle(Paint.Style.FILL);
                    float arriba = Math.min(yA, yC), abajo = Math.max(yA, yC);
                    if (abajo - arriba < 5f) {
                        float mi = (arriba + abajo) / 2f;
                        arriba = mi - 2.5f;
                        abajo = mi + 2.5f;
                    }
                    cv.drawRoundRect(new RectF(cx - cuerpo / 2f, arriba, cx + cuerpo / 2f, abajo), 4, 4, p);
                }
            } else if (tipo == 1) {
                // linea con relleno suave
                Path linea = new Path();
                Path area = new Path();
                for (int i = 0; i < n; i++) {
                    float x = x0 + i * paso;
                    float y = yDe(s.v[i], mn, mx, y0, y1);
                    if (i == 0) {
                        linea.moveTo(x, y);
                        area.moveTo(x, y1);
                        area.lineTo(x, y);
                    } else {
                        linea.lineTo(x, y);
                        area.lineTo(x, y);
                    }
                }
                area.lineTo(x1, y1);
                area.close();
                p.setStyle(Paint.Style.FILL);
                p.setShader(new LinearGradient(0, y0, 0, y1, 0x59470B24, 0x00470B24, Shader.TileMode.CLAMP));
                cv.drawPath(area, p);
                p.setShader(null);
                p.setStyle(Paint.Style.STROKE);
                p.setStrokeWidth(5f);
                p.setStrokeJoin(Paint.Join.ROUND);
                p.setColor(CRIM);
                cv.drawPath(linea, p);
                p.setStyle(Paint.Style.FILL);
                float yu = yDe(s.v[n - 1], mn, mx, y0, y1);
                p.setColor(APRI);
                cv.drawCircle(x1, yu, 12, p);
                p.setColor(ACENTO);
                cv.drawCircle(x1, yu, 8, p);
            } else {
                // barras verticales entre un cierre y el siguiente
                float ancho = Math.max(3f, Math.min(9f, paso * 0.55f));
                for (int i = 1; i < n; i++) {
                    float x = x0 + i * paso;
                    float ya = yDe(s.v[i - 1], mn, mx, y0, y1);
                    float yb = yDe(s.v[i], mn, mx, y0, y1);
                    if (Math.abs(ya - yb) < 6f) {
                        float mi = (ya + yb) / 2f;
                        ya = mi - 3f;
                        yb = mi + 3f;
                    }
                    p.setStyle(Paint.Style.STROKE);
                    p.setStrokeWidth(ancho);
                    p.setColor(i == n - 1 ? ACENTO : CRIM);
                    cv.drawLine(x, ya, x, yb, p);
                }
            }
            p.setStyle(Paint.Style.FILL);

            // fechas
            p.setColor(MUTE);
            p.setTextSize(21);
            p.setTextAlign(Paint.Align.LEFT);
            cv.drawText(fecha(s.f[0]), x0, 380, p);
            p.setTextAlign(Paint.Align.CENTER);
            cv.drawText(fecha(s.f[n / 2]), (x0 + x1) / 2f, 380, p);
            p.setTextAlign(Paint.Align.RIGHT);
            cv.drawText("hoy", x1 + 4, 380, p);
        }

        // estado de las 4 bolsas
        p.setStyle(Paint.Style.FILL);
        p.setTextSize(24);
        p.setTextAlign(Paint.Align.LEFT);
        int cantidad = MercadoDatos.COD.length;
        float ancho4 = (922f - 40f) / cantidad;
        for (int i = 0; i < cantidad; i++) {
            MercadoDatos.Estado ei = MercadoDatos.estado(i, ahora);
            float cx = 40 + i * ancho4;
            boolean activo = i == e.idx;
            p.setColor(ei.abierto ? SUBE : 0xFFB9A58F);
            cv.drawCircle(cx + 8, 428, 8, p);
            p.setTypeface(Typeface.create("sans-serif", activo ? Typeface.BOLD : Typeface.NORMAL));
            p.setColor(activo ? CRIM : MUTE);
            cv.drawText(MercadoDatos.COD[i], cx + 26, 436, p);
        }
        return bm;
    }
}
"""

F[JD + '/ConfigMercados.java'] = r"""package __PKG__;

import android.app.Activity;
import android.appwidget.AppWidgetManager;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.ColorDrawable;
import android.graphics.drawable.GradientDrawable;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.HorizontalScrollView;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

public class ConfigMercados extends Activity {
    static final int CRIM = 0xFF470B24;
    static final int PERI = 0xFFB5BEDD;
    static final int APRI = 0xFFFFEDD5;
    static final int MUTE = 0xFF6B4A5E;

    interface Al {
        void sel(int i);
    }

    SharedPreferences sp;
    float dens;
    LinearLayout col;
    TextView[] chipsDe, chipsA;

    int dp(int v) {
        return (int) (v * dens + 0.5f);
    }

    @Override
    protected void onCreate(Bundle b) {
        super.onCreate(b);
        dens = getResources().getDisplayMetrics().density;
        sp = WidgetDatos.sp(this);
        int id = AppWidgetManager.INVALID_APPWIDGET_ID;
        Bundle ex = getIntent().getExtras();
        if (ex != null) id = ex.getInt(AppWidgetManager.EXTRA_APPWIDGET_ID, AppWidgetManager.INVALID_APPWIDGET_ID);
        if (id != AppWidgetManager.INVALID_APPWIDGET_ID) {
            Intent r = new Intent();
            r.putExtra(AppWidgetManager.EXTRA_APPWIDGET_ID, id);
            setResult(RESULT_OK, r);
        } else {
            setResult(RESULT_CANCELED);
        }
        getWindow().setBackgroundDrawable(new ColorDrawable(0xB0000000));

        FrameLayout raiz = new FrameLayout(this);
        raiz.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                terminar();
            }
        });

        ScrollView sv = new ScrollView(this);
        sv.setVerticalScrollBarEnabled(false);
        GradientDrawable fondo = new GradientDrawable(GradientDrawable.Orientation.TOP_BOTTOM, new int[]{APRI, 0xFFF3E4D8, PERI});
        fondo.setCornerRadius(dp(28));
        sv.setBackground(fondo);
        sv.setClickable(true);
        FrameLayout.LayoutParams lp = new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT, Gravity.CENTER);
        lp.setMargins(dp(16), dp(32), dp(16), dp(32));
        raiz.addView(sv, lp);

        col = new LinearLayout(this);
        col.setOrientation(LinearLayout.VERTICAL);
        col.setPadding(dp(20), dp(20), dp(20), dp(20));
        sv.addView(col, new ViewGroup.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        TextView t = new TextView(this);
        t.setText("Personalizar Mercados");
        t.setTextColor(CRIM);
        t.setTextSize(22);
        t.setTypeface(Typeface.create("sans-serif-medium", Typeface.NORMAL));
        col.addView(t);

        // divisas
        etiqueta("DIVISA");
        int iDe = indice(MercadoDatos.MONEDAS, sp.getString("m_de", "USD"));
        chipsDe = new TextView[MercadoDatos.MONEDAS.length];
        col.addView(chips(MercadoDatos.MONEDAS, iDe, chipsDe, new Al() {
            public void sel(int i) {
                String nueva = MercadoDatos.MONEDAS[i];
                sp.edit().putString("m_de", nueva).apply();
                if (nueva.equals(sp.getString("m_a", "MXN"))) {
                    String otra = nueva.equals("USD") ? "MXN" : "USD";
                    sp.edit().putString("m_a", otra).apply();
                    pintarChips(chipsA, indice(MercadoDatos.MONEDAS, otra));
                }
                cambio(true);
            }
        }));
        etiqueta("CONTRA");
        int iA = indice(MercadoDatos.MONEDAS, sp.getString("m_a", "MXN"));
        chipsA = new TextView[MercadoDatos.MONEDAS.length];
        col.addView(chips(MercadoDatos.MONEDAS, iA, chipsA, new Al() {
            public void sel(int i) {
                String nueva = MercadoDatos.MONEDAS[i];
                sp.edit().putString("m_a", nueva).apply();
                if (nueva.equals(sp.getString("m_de", "USD"))) {
                    String otra = nueva.equals("USD") ? "MXN" : "USD";
                    sp.edit().putString("m_de", otra).apply();
                    pintarChips(chipsDe, indice(MercadoDatos.MONEDAS, otra));
                }
                cambio(true);
            }
        }));

        // grafica
        etiqueta("TIPO DE GRÁFICA");
        col.addView(chips(new String[]{"Velas japonesas", "Líneas", "Barras"}, sp.getInt("m_tipo", 0), null, new Al() {
            public void sel(int i) {
                sp.edit().putInt("m_tipo", i).apply();
                cambio(false);
            }
        }));
        etiqueta("PERIODO");
        col.addView(chips(new String[]{"1 mes", "3 meses", "6 meses"}, sp.getInt("m_rango", 0), null, new Al() {
            public void sel(int i) {
                sp.edit().putInt("m_rango", i).apply();
                cambio(true);
            }
        }));

        // mercado y horario
        etiqueta("MERCADO");
        col.addView(chips(new String[]{"Automático", "Sídney", "Tokio", "Londres", "Nueva York"}, sp.getInt("m_sel", 0), null, new Al() {
            public void sel(int i) {
                sp.edit().putInt("m_sel", i).apply();
                cambio(false);
            }
        }));
        etiqueta("FORMATO DE HORA");
        col.addView(chips(new String[]{"24 horas", "12 horas (AM/PM)"}, sp.getInt("m_f", 0), null, new Al() {
            public void sel(int i) {
                sp.edit().putInt("m_f", i).apply();
                cambio(false);
            }
        }));
        etiqueta("ZONA HORARIA");
        col.addView(chips(new String[]{"Mi hora local", "Ciudad de México", "Nueva York", "Londres", "Tokio", "UTC"}, sp.getInt("m_zona", 0), null, new Al() {
            public void sel(int i) {
                sp.edit().putInt("m_zona", i).apply();
                cambio(false);
            }
        }));

        // botones
        LinearLayout fila = new LinearLayout(this);
        fila.setOrientation(LinearLayout.HORIZONTAL);
        fila.setPadding(0, dp(22), 0, 0);
        TextView act = boton("Actualizar", false);
        act.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Toast.makeText(ConfigMercados.this, "Actualizando…", Toast.LENGTH_SHORT).show();
                cambio(true, true);
            }
        });
        TextView ok = boton("Listo", true);
        ok.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                terminar();
            }
        });
        LinearLayout.LayoutParams l1 = new LinearLayout.LayoutParams(0, dp(46), 1);
        l1.rightMargin = dp(10);
        fila.addView(act, l1);
        fila.addView(ok, new LinearLayout.LayoutParams(0, dp(46), 1));
        col.addView(fila);

        TextView nota = new TextView(this);
        nota.setText("Las velas se arman con los cierres diarios del Banco Central Europeo. Los horarios de las bolsas no incluyen días festivos.");
        nota.setTextColor(MUTE);
        nota.setTextSize(11);
        nota.setPadding(0, dp(14), 0, 0);
        col.addView(nota);

        setContentView(raiz);
        ConvWidgetMercados.repintar(getApplicationContext());
    }

    void terminar() {
        ConvWidgetMercados.repintar(getApplicationContext());
        finish();
    }

    void cambio(boolean conRed) {
        cambio(conRed, false);
    }

    void cambio(final boolean conRed, final boolean forzar) {
        final android.content.Context app = getApplicationContext();
        ConvWidgetMercados.repintar(app);
        if (!conRed) return;
        new Thread(new Runnable() {
            public void run() {
                try {
                    MercadoDatos.refrescar(app, forzar);
                    ConvWidgetMercados.repintar(app);
                } catch (Exception e) {
                }
            }
        }).start();
    }

    static int indice(String[] l, String v) {
        for (int i = 0; i < l.length; i++) if (l[i].equals(v)) return i;
        return 0;
    }

    void etiqueta(String txt) {
        TextView t = new TextView(this);
        t.setText(txt);
        t.setTextColor(MUTE);
        t.setTextSize(11);
        t.setLetterSpacing(0.08f);
        t.setTypeface(Typeface.DEFAULT_BOLD);
        t.setPadding(dp(2), dp(18), 0, dp(8));
        col.addView(t);
    }

    TextView boton(String txt, boolean lleno) {
        TextView t = new TextView(this);
        t.setText(txt);
        t.setGravity(Gravity.CENTER);
        t.setTextSize(15);
        t.setTypeface(Typeface.DEFAULT_BOLD);
        GradientDrawable g = new GradientDrawable();
        g.setCornerRadius(dp(23));
        if (lleno) {
            g.setColor(CRIM);
            t.setTextColor(APRI);
        } else {
            g.setColor(0x00000000);
            g.setStroke(dp(2), CRIM);
            t.setTextColor(CRIM);
        }
        t.setBackground(g);
        return t;
    }

    void pintarChips(TextView[] tv, int s) {
        for (int j = 0; j < tv.length; j++) {
            boolean on = j == s;
            GradientDrawable g = new GradientDrawable();
            g.setCornerRadius(dp(20));
            g.setColor(on ? CRIM : 0x00000000);
            g.setStroke(dp(1), on ? CRIM : 0x80470B24);
            tv[j].setBackground(g);
            tv[j].setTextColor(on ? APRI : CRIM);
        }
    }

    View chips(String[] et, int sel, TextView[] destino, final Al al) {
        HorizontalScrollView hs = new HorizontalScrollView(this);
        hs.setHorizontalScrollBarEnabled(false);
        LinearLayout fila = new LinearLayout(this);
        fila.setOrientation(LinearLayout.HORIZONTAL);
        hs.addView(fila);
        final TextView[] tv = destino != null ? destino : new TextView[et.length];
        for (int i = 0; i < et.length; i++) {
            TextView t = new TextView(this);
            t.setText(et[i]);
            t.setTextSize(14);
            t.setGravity(Gravity.CENTER);
            t.setPadding(dp(14), dp(8), dp(14), dp(8));
            LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
            lp.rightMargin = dp(8);
            fila.addView(t, lp);
            tv[i] = t;
            final int ii = i;
            t.setOnClickListener(new View.OnClickListener() {
                public void onClick(View v) {
                    pintarChips(tv, ii);
                    al.sel(ii);
                }
            });
        }
        pintarChips(tv, sel);
        return hs;
    }
}
"""

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
if True:
    rec = ''
    for clase, nombre, info in (('ConvWidgetGrande', 'Convertidor 4x3', 'widget_grande_info'), ('ConvWidgetChico', 'Tipo de cambio 2x2', 'widget_chico_info'), ('ConvWidgetMercados', 'Mercados 4x2', 'widget_mercados_info')):
        if PKG + '.' + clase in s:
            continue
        rec += '''
        <receiver android:name="%s.%s" android:exported="true" android:label="%s">
            <intent-filter><action android:name="android.appwidget.action.APPWIDGET_UPDATE"/></intent-filter>
            <meta-data android:name="android.appwidget.provider" android:resource="@xml/%s"/>
        </receiver>
''' % (PKG, clase, nombre, info)
    if 'ConfigMercados' not in s:
        rec += '''
        <activity android:name="%s.ConfigMercados" android:exported="true" android:excludeFromRecents="true"
            android:theme="@android:style/Theme.Translucent.NoTitleBar">
            <intent-filter><action android:name="android.appwidget.action.APPWIDGET_CONFIGURE"/></intent-filter>
        </activity>
''' % PKG
    assert '</application>' in s
    s = s.replace('</application>', rec + '    </application>', 1)
    open(mf, 'w', encoding='utf-8').write(s)
print('Widgets agregados en', PKG)
