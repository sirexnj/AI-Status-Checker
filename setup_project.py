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
        versionCode 7
        versionName "1.5.0"
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

"app/src/main/res/drawable/ic_app_logo.xml": """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="#0F172A"
        android:pathData="M0,0h108v108h-108z"/>
    <path
        android:fillColor="#1E293B"
        android:pathData="M54,54m-40,0a40,40 0,1 1,80 0a40,40 0,1 1,-80 0"/>
    <path
        android:strokeColor="#38BDF8"
        android:strokeWidth="3.5"
        android:pathData="M54,18A36,36 0,1 1,18 54A36,36 0,0 1,54 18z"/>
    <path
        android:strokeColor="#10B981"
        android:strokeWidth="5"
        android:strokeLineCap="round"
        android:strokeLineJoin="round"
        android:pathData="M24,56 L38,56 L45,36 L55,74 L64,48 L71,56 L84,56"/>
    <path
        android:fillColor="#38BDF8"
        android:pathData="M54,27 L56,33 L62,35 L56,37 L54,43 L52,37 L46,35 L52,33 Z"/>
</vector>
""",

"app/src/main/AndroidManifest.xml": """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <application
        android:allowBackup="true"
        android:label="AI Status &amp; Ping"
        android:icon="@drawable/ic_app_logo"
        android:roundIcon="@drawable/ic_app_logo"
        android:supportsRtl="true"
        android:theme="@style/Theme.MaterialComponents.DayNight.NoActionBar">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        <activity android:name=".WidgetConfigActivity" android:exported="true" android:label="تنظیمات ویجت">
            <intent-filter>
                <action android:name="android.appwidget.action.APPWIDGET_CONFIGURE" />
            </intent-filter>
        </activity>
        <receiver android:name=".StatusWidget" android:exported="true" android:label="AI Status Widget">
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
    android:minWidth="200dp"
    android:minHeight="110dp"
    android:targetCellWidth="3"
    android:targetCellHeight="2"
    android:minResizeWidth="140dp"
    android:minResizeHeight="70dp"
    android:updatePeriodMillis="0"
    android:initialLayout="@layout/widget_layout"
    android:previewLayout="@layout/widget_layout"
    android:previewImage="@drawable/ic_app_logo"
    android:configure="ir.nimasirex.aistatus.WidgetConfigActivity"
    android:resizeMode="horizontal|vertical"
    android:widgetCategory="home_screen"
    android:widgetFeatures="reconfigurable" />
""",

"app/src/main/res/drawable/widget_bg.xml": """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#EB0F172A" />
    <corners android:radius="20dp" />
    <stroke android:width="1.5dp" android:color="#38BDF8" />
</shape>
""",

"app/src/main/res/layout/widget_layout.xml": """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/widget_root"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="14dp"
    android:background="@drawable/widget_bg"
    android:layoutDirection="rtl">
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:gravity="center_vertical">
        <TextView
            android:id="@+id/widget_title"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="⚡ رادار هوش مصنوعی"
            android:textColor="#38BDF8"
            android:textStyle="bold"
            android:textSize="13sp" />
        <TextView
            android:id="@+id/widget_refresh_hint"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="🔄 بروزرسانی"
            android:textColor="#94A3B8"
            android:textSize="11sp" />
    </LinearLayout>
    <TextView
        android:id="@+id/widget_results"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:text="برای تست لحظه‌ای ضربه بزنید..."
        android:textColor="#F8FAFC"
        android:textSize="12sp"
        android:lineSpacingExtra="4dp" />
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
        l.add(new AIService("gem_web", CATEGORIES[0], "Gemini Web/App", "https://gemini.google.com/app", false));
        l.add(new AIService("ai_studio", CATEGORIES[0], "Google AI Studio", "https://aistudio.google.com", false));
        l.add(new AIService("gem_api", CATEGORIES[0], "Gemini API", "https://generativelanguage.googleapis.com/v1beta/models", true));
        l.add(new AIService("notebook_lm", CATEGORIES[0], "NotebookLM", "https://notebooklm.google.com", false));
        l.add(new AIService("google_labs", CATEGORIES[0], "Google Labs", "https://labs.google/fx", false));
        l.add(new AIService("vertex_ai", CATEGORIES[0], "Vertex AI", "https://console.cloud.google.com/vertex-ai", false));
        l.add(new AIService("chatgpt_web", CATEGORIES[1], "ChatGPT Web", "https://chatgpt.com/backend-api/models", false));
        l.add(new AIService("openai_plat", CATEGORIES[1], "OpenAI Platform", "https://platform.openai.com", false));
        l.add(new AIService("openai_api", CATEGORIES[1], "OpenAI API", "https://api.openai.com/v1/models", false));
        l.add(new AIService("sora", CATEGORIES[1], "Sora Video AI", "https://sora.com", false));
        l.add(new AIService("claude_web", CATEGORIES[2], "Claude Web", "https://claude.ai/api/organizations", false));
        l.add(new AIService("claude_con", CATEGORIES[2], "Anthropic Console", "https://console.anthropic.com", false));
        l.add(new AIService("claude_api", CATEGORIES[2], "Claude API", "https://api.anthropic.com/v1/messages", false));
        l.add(new AIService("perp_web", CATEGORIES[3], "Perplexity Web", "https://www.perplexity.ai", false));
        l.add(new AIService("perp_api", CATEGORIES[3], "Perplexity API", "https://api.perplexity.ai", false));
        l.add(new AIService("ms_copilot", CATEGORIES[4], "Microsoft Copilot", "https://copilot.microsoft.com", false));
        l.add(new AIService("gh_copilot", CATEGORIES[4], "GitHub Copilot", "https://api.githubcopilot.com/_ping", false));
        l.add(new AIService("grok_ai", CATEGORIES[5], "Grok (xAI)", "https://grok.com", false));
        l.add(new AIService("meta_ai", CATEGORIES[5], "Meta AI (Llama)", "https://www.meta.ai", false));
        l.add(new AIService("deepseek", CATEGORIES[6], "DeepSeek Chat", "https://chat.deepseek.com", false));
        l.add(new AIService("huggingface", CATEGORIES[6], "Hugging Face", "https://huggingface.co", false));
        l.add(new AIService("elevenlabs", CATEGORIES[6], "ElevenLabs Audio", "https://api.elevenlabs.io/v1/voices", false));
        l.add(new AIService("replicate", CATEGORIES[6], "Replicate Cloud", "https://api.replicate.com/v1/models", false));
        return l;
    }

    private static String readStream(InputStream is) {
        if (is == null) return "";
        try {
            BufferedReader r = new BufferedReader(new InputStreamReader(is));
            StringBuilder sb = new StringBuilder();
            char[] b = new char[4096];
            int n;
            while ((n = r.read(b)) != -1 && sb.length() < 60000) {
                sb.append(b, 0, n);
            }
            r.close();
            return sb.toString().toLowerCase();
        } catch (Exception e) { return ""; }
    }

    private static boolean isGoogleAiGeoBlocked() {
        try {
            HttpURLConnection nc = (HttpURLConnection) new URL("https://notebooklm.google.com").openConnection();
            nc.setConnectTimeout(4500);
            nc.setReadTimeout(4500);
            nc.setInstanceFollowRedirects(true);
            nc.setRequestProperty("User-Agent", "Mozilla/5.0 (Linux; Android 14) Chrome/124.0.0.0 Mobile");
            int nCode = nc.getResponseCode();
            String nUrl = nc.getURL().toString().toLowerCase();
            String nBody = readStream(nCode >= 400 ? nc.getErrorStream() : nc.getInputStream());
            if (nUrl.contains("unsupported") || nUrl.contains("region") || nUrl.contains("faq") || nBody.contains("not supported")) {
                return true;
            }
        } catch (Exception ignored) {}
        return false;
    }

    public static String checkService(Context ctx, AIService s) {
        SharedPreferences p = ctx.getSharedPreferences("AIPrefs", Context.MODE_PRIVATE);
        String key = p.getString("gemini_api_key", "").trim();
        long t0 = System.currentTimeMillis();
        try {
            String targetUrl = s.url;
            if (s.supportsApiKey && !key.isEmpty()) {
                targetUrl = "https://generativelanguage.googleapis.com/v1beta/models?key=" + key;
            }

            HttpURLConnection c = (HttpURLConnection) new URL(targetUrl).openConnection();
            c.setConnectTimeout(6000); c.setReadTimeout(6000); c.setInstanceFollowRedirects(true);
            c.setRequestProperty("User-Agent", "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36");

            int code = c.getResponseCode();
            String snip = readStream(code >= 400 ? c.getErrorStream() : c.getInputStream());
            String fu = c.getURL().toString().toLowerCase();

            if (s.category.equals(CATEGORIES[0]) && !s.id.equals("vertex_ai")) {
                if (isGoogleAiGeoBlocked()) {
                    long ping = System.currentTimeMillis() - t0;
                    return "🟡 تحریم آی‌پی (" + ping + "ms)";
                }
            }

            long ping = System.currentTimeMillis() - t0;

            if (fu.contains("unsupported") || fu.contains("region") || fu.contains("faq") || fu.contains("unavailable") ||
                snip.contains("country isn't supported") ||
                snip.contains("location is not supported") ||
                snip.contains("not available in your country") ||
                snip.contains("unsupported_country") ||
                snip.contains("region_not_supported") ||
                snip.contains("gradually expanding") ||
                snip.contains("access denied") ||
                snip.contains("error 1020")) {
                return "🟡 تحریم آی‌پی (" + ping + "ms)";
            }

            // If Gemini API returns 403 only because API key is missing, but geo-check passed, it's open!
            if (s.supportsApiKey && key.isEmpty() && (code == 403 || code == 400)) {
                return "🟢 درگاه باز (" + ping + "ms)";
            }

            if (code == 403 || code == 451) {
                return "🟡 محدودیت آی‌پی (" + ping + "ms)";
            }

            if (s.supportsApiKey && !key.isEmpty() && code == 200) {
                return "🟢 متصل با کلید (" + ping + "ms)";
            }

            if ((code >= 200 && code < 400) || code == 401 || code == 400 || code == 405) {
                return "🟢 متصل (" + ping + "ms)";
            }
            return "🟡 کد " + code + " (" + ping + "ms)";
        } catch (Exception e) { return "🔴 قطع / عدم دسترسی"; }
    }
}
""",

"app/src/main/java/ir/nimasirex/aistatus/MainActivity.java": """package ir.nimasirex.aistatus;
import android.content.*;
import android.graphics.*;
import android.graphics.drawable.GradientDrawable;
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

    private GradientDrawable makeCard(String bgHex, String strokeHex, int radius) {
        GradientDrawable gd = new GradientDrawable();
        gd.setColor(Color.parseColor(bgHex));
        gd.setCornerRadius(radius);
        if (strokeHex != null) gd.setStroke(2, Color.parseColor(strokeHex));
        return gd;
    }

    @Override protected void onCreate(Bundle b) {
        super.onCreate(b);
        ScrollView sv = new ScrollView(this);
        sv.setBackgroundColor(Color.parseColor("#0B1120"));
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(40, 64, 40, 64);
        root.setLayoutDirection(View.LAYOUT_DIRECTION_RTL);
        sv.addView(root);

        // Header Card
        LinearLayout headerCard = new LinearLayout(this);
        headerCard.setOrientation(LinearLayout.VERTICAL);
        headerCard.setPadding(36, 36, 36, 36);
        headerCard.setBackground(makeCard("#1E293B", "#38BDF8", 32));
        root.addView(headerCard);

        TextView h = new TextView(this);
        h.setText("⚡ رادار و پینگ‌سنج هوش مصنوعی");
        h.setTextColor(Color.parseColor("#38BDF8"));
        h.setTextSize(19);
        h.setTypeface(null, Typeface.BOLD);
        h.setGravity(Gravity.CENTER);
        headerCard.addView(h);

        TextView sub = new TextView(this);
        sub.setText("بررسی دقیق اتصال، پینگ و محدودیت آی‌پی سرورهای AI");
        sub.setTextColor(Color.parseColor("#94A3B8"));
        sub.setTextSize(12);
        sub.setGravity(Gravity.CENTER);
        sub.setPadding(0, 10, 0, 24);
        headerCard.addView(sub);

        Button wBtn = new Button(this);
        wBtn.setText("➕ تنظیم و افزودن ویجت به صفحه اصلی");
        wBtn.setTextColor(Color.WHITE);
        wBtn.setTypeface(null, Typeface.BOLD);
        wBtn.setBackground(makeCard("#059669", null, 24));
        headerCard.addView(wBtn);
        wBtn.setOnClickListener(v -> startActivity(new Intent(this, WidgetConfigActivity.class)));

        // Categories Card
        LinearLayout catCard = new LinearLayout(this);
        catCard.setOrientation(LinearLayout.VERTICAL);
        catCard.setPadding(32, 28, 32, 28);
        catCard.setBackground(makeCard("#1E293B", "#334155", 28));
        LinearLayout.LayoutParams cp = new LinearLayout.LayoutParams(-1, -2);
        cp.setMargins(0, 28, 0, 28);
        root.addView(catCard, cp);

        TextView sh = new TextView(this);
        sh.setText("۱. سرویس‌های مورد نظر برای تست:");
        sh.setTextColor(Color.parseColor("#F8FAFC"));
        sh.setTypeface(null, Typeface.BOLD);
        sh.setPadding(0, 0, 0, 12);
        catCard.addView(sh);

        for (int i = 0; i < ServiceData.CATEGORIES.length; i++) {
            CheckBox cb = new CheckBox(this);
            cb.setText(ServiceData.CATEGORIES[i]);
            cb.setTextColor(Color.parseColor("#E2E8F0"));
            cb.setChecked(i == 0);
            catBoxes.add(cb);
            catCard.addView(cb);
        }

        // API Key Card
        LinearLayout apiCard = new LinearLayout(this);
        apiCard.setOrientation(LinearLayout.VERTICAL);
        apiCard.setPadding(32, 24, 32, 24);
        apiCard.setBackground(makeCard("#1E293B", "#334155", 28));
        root.addView(apiCard);

        TextView at = new TextView(this);
        at.setText("🔑 کلید اختصاصی Gemini API (اختیاری):");
        at.setTextColor(Color.parseColor("#94A3B8"));
        at.setTextSize(13);
        apiCard.addView(at);

        SharedPreferences prefs = getSharedPreferences("AIPrefs", MODE_PRIVATE);
        apiIn = new EditText(this);
        apiIn.setHint("بدون کلید هم تست تحریم انجام می‌شود...");
        apiIn.setHintTextColor(Color.parseColor("#64748B"));
        apiIn.setTextColor(Color.WHITE);
        apiIn.setTextSize(13);
        apiIn.setText(prefs.getString("gemini_api_key", ""));
        apiCard.addView(apiIn);

        // Start Test Button
        Button btn = new Button(this);
        btn.setText("🚀 شروع تست هوشمند سرویس‌ها");
        btn.setTextColor(Color.WHITE);
        btn.setTextSize(15);
        btn.setTypeface(null, Typeface.BOLD);
        btn.setBackground(makeCard("#0284C7", null, 26));
        LinearLayout.LayoutParams bp = new LinearLayout.LayoutParams(-1, -2);
        bp.setMargins(0, 32, 0, 24);
        root.addView(btn, bp);

        resBox = new LinearLayout(this);
        resBox.setOrientation(LinearLayout.VERTICAL);
        root.addView(resBox);

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
            TextView ch = new TextView(this);
            ch.setText("▪ " + cat);
            ch.setTextColor(Color.parseColor("#38BDF8"));
            ch.setTypeface(null, Typeface.BOLD);
            ch.setPadding(8, 24, 8, 12);
            resBox.addView(ch);

            for (ServiceData.AIService s : ServiceData.getAllServices()) {
                if (s.category.equals(cat)) {
                    LinearLayout row = new LinearLayout(this);
                    row.setPadding(28, 22, 28, 22);
                    row.setGravity(Gravity.CENTER_VERTICAL);
                    row.setBackground(makeCard("#1E293B", "#334155", 20));
                    LinearLayout.LayoutParams rp = new LinearLayout.LayoutParams(-1, -2);
                    rp.setMargins(0, 0, 0, 14);

                    TextView nt = new TextView(this);
                    nt.setText(s.name);
                    nt.setTextColor(Color.WHITE);
                    nt.setTypeface(null, Typeface.BOLD);
                    nt.setTextSize(13);
                    nt.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1f));

                    TextView st = new TextView(this);
                    st.setText("⏳ در حال تست...");
                    st.setTextColor(Color.parseColor("#FACC15"));
                    st.setTextSize(12);

                    row.addView(nt);
                    row.addView(st);
                    resBox.addView(row, rp);
                    resViews.put(s.id, st);

                    exec.execute(() -> {
                        String r = ServiceData.checkService(MainActivity.this, s);
                        runOnUiThread(() -> {
                            TextView tv = resViews.get(s.id);
                            if (tv != null) {
                                tv.setText(r);
                                tv.setTextColor(r.startsWith("🟢") ? Color.parseColor("#4ADE80") : r.startsWith("🟡") ? Color.parseColor("#FACC15") : Color.parseColor("#F87171"));
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
import android.graphics.drawable.GradientDrawable;
import android.os.Build;
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

        ScrollView sv = new ScrollView(this); sv.setBackgroundColor(Color.parseColor("#0B1120"));
        LinearLayout root = new LinearLayout(this); root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(40, 60, 40, 60); root.setLayoutDirection(View.LAYOUT_DIRECTION_RTL); sv.addView(root);

        TextView t = new TextView(this); t.setText("انتخاب سرویس‌های ویجت صفحه اصلی");
        t.setTextColor(Color.parseColor("#38BDF8")); t.setTextSize(17); t.setTypeface(null, Typeface.BOLD);
        t.setPadding(0, 0, 0, 16); root.addView(t);

        Set<String> saved = getSharedPreferences("WidgetPrefs", MODE_PRIVATE).getStringSet("w_default", null);

        String cur = "";
        for (ServiceData.AIService s : ServiceData.getAllServices()) {
            if (!s.category.equals(cur)) {
                cur = s.category;
                TextView ct = new TextView(this); ct.setText("▪ " + cur); ct.setTextColor(Color.parseColor("#38BDF8"));
                ct.setTypeface(null, Typeface.BOLD); ct.setPadding(0, 22, 0, 6); root.addView(ct);
            }
            CheckBox cb = new CheckBox(this); cb.setText(s.name); cb.setTag(s.id); cb.setTextColor(Color.WHITE);
            if (saved != null) cb.setChecked(saved.contains(s.id));
            else if (s.id.equals("gem_web") || s.id.equals("chatgpt_web") || s.id.equals("grok_ai")) cb.setChecked(true);
            boxes.add(cb); root.addView(cb);
        }

        GradientDrawable gd = new GradientDrawable();
        gd.setColor(Color.parseColor("#059669"));
        gd.setCornerRadius(24);

        Button btn = new Button(this); btn.setText("✅ ذخیره و بروزرسانی ویجت");
        btn.setBackground(gd); btn.setTextColor(Color.WHITE); btn.setTypeface(null, Typeface.BOLD);
        LinearLayout.LayoutParams bp = new LinearLayout.LayoutParams(-1, -2);
        bp.setMargins(0, 32, 0, 16);
        root.addView(btn, bp);

        btn.setOnClickListener(v -> {
            Set<String> ids = new HashSet<>();
            for (CheckBox cb : boxes) if (cb.isChecked()) ids.add((String) cb.getTag());
            if (ids.isEmpty()) { Toast.makeText(this, "حداقل یک سرویس انتخاب کنید", Toast.LENGTH_SHORT).show(); return; }

            SharedPreferences.Editor ed = getSharedPreferences("WidgetPrefs", MODE_PRIVATE).edit();
            ed.putStringSet("w_default", ids);
            if (widgetId != AppWidgetManager.INVALID_APPWIDGET_ID) ed.putStringSet("w_" + widgetId, ids);
            ed.apply();

            AppWidgetManager m = AppWidgetManager.getInstance(this);
            ComponentName cn = new ComponentName(this, StatusWidget.class);

            if (widgetId != AppWidgetManager.INVALID_APPWIDGET_ID) {
                StatusWidget.updateAppWidget(this, m, widgetId);
                Intent res = new Intent(); res.putExtra(AppWidgetManager.EXTRA_APPWIDGET_ID, widgetId);
                setResult(RESULT_OK, res); finish();
            } else {
                int[] existing = m.getAppWidgetIds(cn);
                if (existing != null && existing.length > 0) {
                    for (int id : existing) StatusWidget.updateAppWidget(this, m, id);
                    Toast.makeText(this, "ویجت شما روی صفحه اصلی بروزرسانی شد!", Toast.LENGTH_SHORT).show();
                } else if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O && m.isRequestPinAppWidgetSupported()) {
                    m.requestPinAppWidget(cn, null, null);
                }
                finish();
            }
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
            AppWidgetManager m = AppWidgetManager.getInstance(c);
            if (id != AppWidgetManager.INVALID_APPWIDGET_ID) updateAppWidget(c, m, id);
            else {
                for (int wid : m.getAppWidgetIds(new ComponentName(c, StatusWidget.class))) updateAppWidget(c, m, wid);
            }
        }
    }
    public static void updateAppWidget(Context c, AppWidgetManager m, int id) {
        RemoteViews v = new RemoteViews(c.getPackageName(), R.layout.widget_layout);
        v.setTextViewText(R.id.widget_results, "⏳ در حال تست لحظه‌ای سرورها...");
        Intent i = new Intent(c, StatusWidget.class); i.setAction(ACT); i.putExtra(AppWidgetManager.EXTRA_APPWIDGET_ID, id);
        PendingIntent pi = PendingIntent.getBroadcast(c, id, i, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        v.setOnClickPendingIntent(R.id.widget_root, pi);
        m.updateAppWidget(id, v);

        Executors.newSingleThreadExecutor().execute(() -> {
            SharedPreferences p = c.getSharedPreferences("WidgetPrefs", Context.MODE_PRIVATE);
            Set<String> ids = p.getStringSet("w_" + id, null);
            if (ids == null || ids.isEmpty()) ids = p.getStringSet("w_default", null);
            if (ids == null || ids.isEmpty()) ids = new HashSet<>(Arrays.asList("gem_web", "chatgpt_web", "grok_ai"));
            StringBuilder sb = new StringBuilder();
            for (ServiceData.AIService s : ServiceData.getAllServices()) {
                if (ids.contains(s.id)) {
                    if (sb.length() > 0) sb.append("\\n");
                    // Use Left-to-Right mark and clean separator so English & Persian never break lines awkwardly
                    String status = ServiceData.checkService(c, s);
                    sb.append(status).append("  ⬅  ").append(s.name);
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
