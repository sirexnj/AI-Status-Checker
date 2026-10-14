import os

files = {
"settings.gradle": """pluginManagement {
    repositories { google(); mavenCentral(); gradlePluginPortal() }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories { google(); mavenCentral() }
}
rootProject.name = "AIStatusChecker"
include ':app'
""",

"build.gradle": """plugins {
    id 'com.android.application' version '8.2.2' apply false
}
""",

"gradle.properties": """org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
""",

"app/build.gradle": """plugins { id 'com.android.application' }
android {
    namespace 'ir.nimasirex.aistatus'
    compileSdk 34
    defaultConfig {
        applicationId "ir.nimasirex.aistatus"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0.0"
    }
    signingConfigs {
        release {
            storeFile file("../release-key.jks")
            storePassword "123456"
            keyAlias "my-key"
            keyPassword "123456"
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled false
            shrinkResources false
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }
}
dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
}
""",

"app/src/main/AndroidManifest.xml": """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <application
        android:allowBackup="true"
        android:label="AI Status &amp; Ping"
        android:icon="@android:drawable/ic_dialog_info"
        android:supportsRtl="true"
        android:theme="@style/Theme.MaterialComponents.DayNight.DarkActionBar">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        <activity android:name=".WidgetConfigActivity" android:exported="true" android:label="انتخاب سرویس‌های ویجت">
            <intent-filter>
                <action android:name="android.appwidget.action.APPWIDGET_CONFIGURE" />
            </intent-filter>
        </activity>
        <receiver android:name=".StatusWidget" android:exported="true" android:label="ویجت وضعیت هوش مصنوعی">
            <intent-filter>
                <action android:name="android.appwidget.action.APPWIDGET_UPDATE" />
                <action android:name="ir.nimasirex.aistatus.ACTION_REFRESH_WIDGET" />
            </intent-filter>
            <meta-data android:name="android.appwidget.provider" android:resource="@xml/widget_info" />
        </receiver>
    </application>
</manifest>
""",

"app/src/main/res/xml/widget_info.xml": """<?xml version="1.0" encoding="utf-8"?>
<appwidget-provider xmlns:android="http://schemas.android.com/apk/res/android"
    android:minWidth="180dp"
    android:minHeight="110dp"
    android:updatePeriodMillis="0"
    android:initialLayout="@layout/widget_layout"
    android:configure="ir.nimasirex.aistatus.WidgetConfigActivity"
    android:resizeMode="horizontal|vertical"
    android:widgetCategory="home_screen" />
""",

"app/src/main/res/drawable/widget_bg.xml": """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#E61E293B" />
    <corners android:radius="16dp" />
    <stroke android:width="1dp" android:color="#475569" />
</shape>
""",

"app/src/main/res/layout/widget_layout.xml": """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/widget_root"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="12dp"
    android:background="@drawable/widget_bg"
    android:layoutDirection="rtl">
    <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="horizontal">
        <TextView android:id="@+id/widget_title" android:layout_width="0dp" android:layout_height="wrap_content" android:layout_weight="1" android:text="وضعیت هوش مصنوعی" android:textColor="#38BDF8" android:textStyle="bold" android:textSize="13sp" />
        <TextView android:id="@+id/widget_refresh_hint" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="🔄 تست لحظه‌ای" android:textColor="#94A3B8" android:textSize="11sp" />
    </LinearLayout>
    <TextView android:id="@+id/widget_results" android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="8dp" android:text="برای بررسی کلیک کنید..." android:textColor="#F8FAFC" android:textSize="12sp" android:lineSpacingExtra="3dp" />
</LinearLayout>
""",

"app/src/main/java/ir/nimasirex/aistatus/ServiceData.java": """package ir.nimasirex.aistatus;
import android.content.Context;
import android.content.SharedPreferences;
import java.io.*;
import java.net.*;
import java.util.*;

public class ServiceData {
    public static class AIService {
        public String id, category, name, url;
        public boolean supportsApiKey;
        public AIService(String id, String c, String n, String u, boolean k) {
            this.id = id; this.category = c; this.name = n; this.url = u; this.supportsApiKey = k;
        }
    }
    public static final String[] CATEGORIES = {
        "خانواده گوگل و جمینای (Google & Gemini)",
        "خانواده اوپن‌ای‌آی (OpenAI / ChatGPT)",
        "خانواده آنتروپیک (Anthropic / Claude)",
        "خانواده پرپلکسیتی (Perplexity AI)",
        "خانواده مایکروسافت و گیت‌هاب (Copilot)",
        "خانواده ایکس و متا (Grok & Meta AI)",
        "پلتفرم‌های ابزار و مدل‌های مکمل"
    };
    public static List<AIService> getAllServices() {
        List<AIService> l = new ArrayList<>();
        l.add(new AIService("gem_web", CATEGORIES[0], "Gemini Web/App", "https://gemini.google.com", false));
        l.add(new AIService("ai_studio", CATEGORIES[0], "Google AI Studio", "https://aistudio.google.com", false));
        l.add(new AIService("gem_api", CATEGORIES[0], "Gemini API (مستقیم)", "https://generativelanguage.googleapis.com", true));
        l.add(new AIService("notebook_lm", CATEGORIES[0], "NotebookLM", "https://notebooklm.google.com", false));
        l.add(new AIService("google_labs", CATEGORIES[0], "Google Labs (Imagen/Veo)", "https://labs.google", false));
        l.add(new AIService("vertex_ai", CATEGORIES[0], "Vertex AI", "https://cloud.google.com/vertex-ai", false));
        l.add(new AIService("chatgpt_web", CATEGORIES[1], "ChatGPT Web/App", "https://chatgpt.com", false));
        l.add(new AIService("openai_plat", CATEGORIES[1], "OpenAI Platform", "https://platform.openai.com", false));
        l.add(new AIService("openai_api", CATEGORIES[1], "OpenAI API", "https://api.openai.com", false));
        l.add(new AIService("sora", CATEGORIES[1], "Sora Video AI", "https://sora.com", false));
        l.add(new AIService("claude_web", CATEGORIES[2], "Claude Web/App", "https://claude.ai", false));
        l.add(new AIService("claude_con", CATEGORIES[2], "Anthropic Console", "https://console.anthropic.com", false));
        l.add(new AIService("claude_api", CATEGORIES[2], "Claude API", "https://api.anthropic.com", false));
        l.add(new AIService("perp_web", CATEGORIES[3], "Perplexity Web/App", "https://www.perplexity.ai", false));
        l.add(new AIService("perp_api", CATEGORIES[3], "Perplexity API", "https://api.perplexity.ai", false));
        l.add(new AIService("ms_copilot", CATEGORIES[4], "Microsoft Copilot", "https://copilot.microsoft.com", false));
        l.add(new AIService("gh_copilot", CATEGORIES[4], "GitHub Copilot", "https://github.com/features/copilot", false));
        l.add(new AIService("grok_ai", CATEGORIES[5], "Grok (xAI)", "https://x.ai", false));
        l.add(new AIService("meta_ai", CATEGORIES[5], "Meta AI (Llama)", "https://www.meta.ai", false));
        l.add(new AIService("deepseek", CATEGORIES[6], "DeepSeek Chat", "https://chat.deepseek.com", false));
        l.add(new AIService("huggingface", CATEGORIES[6], "Hugging Face", "https://huggingface.co", false));
        l.add(new AIService("elevenlabs", CATEGORIES[6], "ElevenLabs Audio", "https://elevenlabs.io", false));
        l.add(new AIService("replicate", CATEGORIES[6], "Replicate Cloud", "https://replicate.com", false));
        return l;
    }
    public static String checkService(Context ctx, AIService s) {
        SharedPreferences p = ctx.getSharedPreferences("AIPrefs", Context.MODE_PRIVATE);
        String key = p.getString("gemini_api_key", "").trim();
        long t0 = System.currentTimeMillis();
        try {
            String u = (s.supportsApiKey && !key.isEmpty()) ? "https://generativelanguage.googleapis.com/v1beta/models?key=" + key : s.url;
            HttpURLConnection c = (HttpURLConnection) new URL(u).openConnection();
            c.setConnectTimeout(6500); c.setReadTimeout(6500); c.setInstanceFollowRedirects(true);
            c.setRequestProperty("User-Agent", "Mozilla/5.0 (Linux; Android 14) Chrome/122.0.0.0 Mobile");
            int code = c.getResponseCode();
            long ping = System.currentTimeMillis() - t0;
            String fu = c.getURL().toString().toLowerCase();
            if (fu.contains("unsupported") || fu.contains("region") || fu.contains("faq")) return "⚠️ محدودیت آی‌پی | " + ping + "ms";
            String snip = "";
            try {
                InputStream is = (code >= 400) ? c.getErrorStream() : c.getInputStream();
                if (is != null) {
                    BufferedReader r = new BufferedReader(new InputStreamReader(is));
                    char[] b = new char[1024]; int n = r.read(b); r.close();
                    if (n > 0) snip = new String(b, 0, n).toLowerCase();
                }
            } catch (Exception ignored) {}
            if (code == 403 || code == 451 || snip.contains("not supported") || snip.contains("unsupported_country")) return "⚠️ محدودیت آی‌پی (403) | " + ping + "ms";
            if (s.supportsApiKey && key.isEmpty() && (code == 400 || code == 404 || code == 401)) return "✅ درگاه باز (" + ping + "ms)";
            if ((code >= 200 && code < 400) || code == 401 || code == 405) return "✅ متصل (" + ping + "ms)";
            return "⚠️ کد " + code + " (" + ping + "ms)";
        } catch (Exception e) { return "❌ قطع / عدم دسترسی"; }
    }
}
""",

"app/src/main/java/ir/nimasirex/aistatus/MainActivity.java": """package ir.nimasirex.aistatus;
import android.content.SharedPreferences;
import android.graphics.*;
import android.os.Bundle;
import android.view.*;
import android.widget.*;
import androidx.appcompat.app.AppCompatActivity;
import java.util.*;
import java.util.concurrent.*;

public class MainActivity extends AppCompatActivity {
    private final List<CheckBox> catBoxes = new ArrayList<>();
    private final Map<String, TextView> resViews = new HashMap<>();
    private LinearLayout resBox;
    private EditText apiIn;
    private final ExecutorService exec = Executors.newFixedThreadPool(6);

    @Override protected void onCreate(Bundle b) {
        super.onCreate(b);
        ScrollView sv = new ScrollView(this); sv.setBackgroundColor(Color.parseColor("#0F172A"));
        LinearLayout root = new LinearLayout(this); root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(36, 36, 36, 48); root.setLayoutDirection(View.LAYOUT_DIRECTION_RTL);
        sv.addView(root);

        TextView h = new TextView(this); h.setText("پینگ‌سنج و وضعیت سرورهای هوش مصنوعی");
        h.setTextColor(Color.parseColor("#38BDF8")); h.setTextSize(18); h.setTypeface(null, Typeface.BOLD);
        h.setGravity(Gravity.CENTER); root.addView(h);

        TextView sh = new TextView(this); sh.setText("۱. خانواده‌های مورد نظر را انتخاب کنید:");
        sh.setTextColor(Color.parseColor("#E2E8F0")); sh.setPadding(0, 24, 0, 10); root.addView(sh);

        for (int i = 0; i < ServiceData.CATEGORIES.length; i++) {
            CheckBox cb = new CheckBox(this); cb.setText(ServiceData.CATEGORIES[i]);
            cb.setTextColor(Color.WHITE); cb.setChecked(i == 0);
            catBoxes.add(cb); root.addView(cb);
        }

        TextView at = new TextView(this); at.setText("🔑 کلید اختصاصی Gemini API Key (اختیاری):");
        at.setTextColor(Color.parseColor("#94A3B8")); at.setPadding(0, 20, 0, 6); root.addView(at);

        SharedPreferences prefs = getSharedPreferences("AIPrefs", MODE_PRIVATE);
        apiIn = new EditText(this); apiIn.setHint("بدون کلید هم تست درگاه انجام می‌شود...");
        apiIn.setHintTextColor(Color.parseColor("#64748B")); apiIn.setTextColor(Color.WHITE);
        apiIn.setText(prefs.getString("gemini_api_key", "")); root.addView(apiIn);

        Button btn = new Button(this); btn.setText("🚀 شروع تست سرویس‌های انتخابی");
        btn.setBackgroundColor(Color.parseColor("#0284C7")); btn.setTextColor(Color.WHITE);
        root.addView(btn);

        resBox = new LinearLayout(this); resBox.setOrientation(LinearLayout.VERTICAL); root.addView(resBox);
        btn.setOnClickListener(v -> runTests());
        setContentView(sv);
    }

    private void runTests() {
        getSharedPreferences("AIPrefs", MODE_PRIVATE).edit().putString("gemini_api_key", apiIn.getText().toString().trim()).apply();
        resBox.removeAllViews(); resViews.clear();
        List<String> sel = new ArrayList<>();
        for (CheckBox cb : catBoxes) if (cb.isChecked()) sel.add(cb.getText().toString());
        if (sel.isEmpty()) { Toast.makeText(this, "حداقل یک دسته را انتخاب کنید", Toast.LENGTH_SHORT).show(); return; }

        for (String cat : sel) {
            TextView ch = new TextView(this); ch.setText("▪ " + cat);
            ch.setTextColor(Color.parseColor("#38BDF8")); ch.setTypeface(null, Typeface.BOLD);
            ch.setPadding(0, 20, 0, 8); resBox.addView(ch);

            for (ServiceData.AIService s : ServiceData.getAllServices()) {
                if (s.category.equals(cat)) {
                    LinearLayout row = new LinearLayout(this); row.setPadding(16, 14, 16, 14);
                    row.setBackgroundColor(Color.parseColor("#1E293B"));
                    TextView nt = new TextView(this); nt.setText(s.name); nt.setTextColor(Color.WHITE);
                    nt.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1f));
                    TextView st = new TextView(this); st.setText("⏳ در حال تست..."); st.setTextColor(Color.YELLOW);
                    row.addView(nt); row.addView(st); resBox.addView(row);
                    resViews.put(s.id, st);
                    exec.execute(() -> {
                        String r = ServiceData.checkService(MainActivity.this, s);
                        runOnUiThread(() -> {
                            TextView tv = resViews.get(s.id);
                            if (tv != null) {
                                tv.setText(r);
                                tv.setTextColor(r.startsWith("✅") ? Color.parseColor("#4ADE80") : r.startsWith("⚠️") ? Color.parseColor("#FACC15") : Color.parseColor("#F87171"));
                            }
                        });
                    });
                }
            }
        }
    }
}
""",

"app/src/main/java/ir/nimasirex/aistatus/WidgetConfigActivity.java": """package ir.nimasirex.aistatus;
import android.appwidget.AppWidgetManager;
import android.content.*;
import android.graphics.*;
import android.os.Bundle;
import android.view.View;
import android.widget.*;
import androidx.appcompat.app.AppCompatActivity;
import java.util.*;

public class WidgetConfigActivity extends AppCompatActivity {
    private int widgetId = AppWidgetManager.INVALID_APPWIDGET_ID;
    private final List<CheckBox> boxes = new ArrayList<>();

    @Override protected void onCreate(Bundle b) {
        super.onCreate(b); setResult(RESULT_CANCELED);
        Bundle ex = getIntent().getExtras();
        if (ex != null) widgetId = ex.getInt(AppWidgetManager.EXTRA_APPWIDGET_ID, AppWidgetManager.INVALID_APPWIDGET_ID);
        if (widgetId == AppWidgetManager.INVALID_APPWIDGET_ID) { finish(); return; }

        ScrollView sv = new ScrollView(this); sv.setBackgroundColor(Color.parseColor("#0F172A"));
        LinearLayout root = new LinearLayout(this); root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(36, 36, 36, 48); root.setLayoutDirection(View.LAYOUT_DIRECTION_RTL); sv.addView(root);

        TextView t = new TextView(this); t.setText("کدام سرویس‌ها روی ویجت نمایش داده شوند؟");
        t.setTextColor(Color.parseColor("#38BDF8")); t.setTextSize(16); t.setTypeface(null, Typeface.BOLD); root.addView(t);

        String cur = "";
        for (ServiceData.AIService s : ServiceData.getAllServices()) {
            if (!s.category.equals(cur)) {
                cur = s.category;
                TextView ct = new TextView(this); ct.setText(cur); ct.setTextColor(Color.parseColor("#94A3B8"));
                ct.setPadding(0, 18, 0, 4); root.addView(ct);
            }
            CheckBox cb = new CheckBox(this); cb.setText(s.name); cb.setTag(s.id); cb.setTextColor(Color.WHITE);
            if (s.id.equals("gem_web") || s.id.equals("gem_api")) cb.setChecked(true);
            boxes.add(cb); root.addView(cb);
        }

        Button btn = new Button(this); btn.setText("✅ ساخت ویجت روی صفحه");
        btn.setBackgroundColor(Color.parseColor("#10B981")); btn.setTextColor(Color.WHITE); root.addView(btn);
        btn.setOnClickListener(v -> {
            Set<String> ids = new HashSet<>();
            for (CheckBox cb : boxes) if (cb.isChecked()) ids.add((String) cb.getTag());
            if (ids.isEmpty()) { Toast.makeText(this, "حداقل یک سرویس انتخاب کنید", Toast.LENGTH_SHORT).show(); return; }
            getSharedPreferences("WidgetPrefs", MODE_PRIVATE).edit().putStringSet("w_" + widgetId, ids).apply();
            StatusWidget.updateAppWidget(this, AppWidgetManager.getInstance(this), widgetId);
            Intent res = new Intent(); res.putExtra(AppWidgetManager.EXTRA_APPWIDGET_ID, widgetId);
            setResult(RESULT_OK, res); finish();
        });
        setContentView(sv);
    }
}
""",

"app/src/main/java/ir/nimasirex/aistatus/StatusWidget.java": """package ir.nimasirex.aistatus;
import android.app.PendingIntent;
import android.appwidget.*;
import android.content.*;
import android.widget.RemoteViews;
import java.util.*;
import java.util.concurrent.Executors;

public class StatusWidget extends AppWidgetProvider {
    public static final String ACT = "ir.nimasirex.aistatus.ACTION_REFRESH_WIDGET";
    @Override public void onUpdate(Context c, AppWidgetManager m, int[] ids) {
        for (int id : ids) updateAppWidget(c, m, id);
    }
    @Override public void onReceive(Context c, Intent i) {
        super.onReceive(c, i);
        if (ACT.equals(i.getAction())) {
            int id = i.getIntExtra(AppWidgetManager.EXTRA_APPWIDGET_ID, AppWidgetManager.INVALID_APPWIDGET_ID);
            if (id != AppWidgetManager.INVALID_APPWIDGET_ID) updateAppWidget(c, AppWidgetManager.getInstance(c), id);
        }
    }
    public static void updateAppWidget(Context c, AppWidgetManager m, int id) {
        RemoteViews v = new RemoteViews(c.getPackageName(), R.layout.widget_layout);
        v.setTextViewText(R.id.widget_results, "⏳ در حال بررسی لحظه‌ای سرورها...");
        Intent i = new Intent(c, StatusWidget.class); i.setAction(ACT); i.putExtra(AppWidgetManager.EXTRA_APPWIDGET_ID, id);
        PendingIntent pi = PendingIntent.getBroadcast(c, id, i, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        v.setOnClickPendingIntent(R.id.widget_root, pi);
        m.updateAppWidget(id, v);

        Executors.newSingleThreadExecutor().execute(() -> {
            Set<String> ids = c.getSharedPreferences("WidgetPrefs", Context.MODE_PRIVATE).getStringSet("w_" + id, null);
            if (ids == null || ids.isEmpty()) ids = new HashSet<>(Arrays.asList("gem_web", "gem_api"));
            StringBuilder sb = new StringBuilder();
            for (ServiceData.AIService s : ServiceData.getAllServices()) {
                if (ids.contains(s.id)) {
                    if (sb.length() > 0) sb.append("\\n");
                    sb.append("• ").append(s.name).append(": ").append(ServiceData.checkService(c, s));
                }
            }
            RemoteViews uv = new RemoteViews(c.getPackageName(), R.layout.widget_layout);
            uv.setTextViewText(R.id.widget_results, sb.toString());
            uv.setOnClickPendingIntent(R.id.widget_root, pi);
            m.updateAppWidget(id, uv);
        });
    }
}
"""
}

for path, content in files.items():
    d = os.path.dirname(path)
    if d: os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f: f.write(content)
print("Done!")
