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
        versionCode 8
        versionName "1.6.0"
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
    implementation 'androidx.drawerlayout:drawerlayout:1.2.0'
}
""",

"app/src/main/res/drawable/ic_app_logo.xml": """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path android:fillColor="#0F172A" android:pathData="M0,0h108v108h-108z"/>
    <path android:fillColor="#1E293B" android:pathData="M54,54m-40,0a40,40 0,1 1,80 0a40,40 0,1 1,-80 0"/>
    <path android:strokeColor="#38BDF8" android:strokeWidth="3.5" android:pathData="M54,18A36,36 0,1 1,18 54A36,36 0,0 1,54 18z"/>
    <path android:strokeColor="#10B981" android:strokeWidth="5" android:strokeLineCap="round" android:strokeLineJoin="round" android:pathData="M24,56 L38,56 L45,36 L55,74 L64,48 L71,56 L84,56"/>
    <path android:fillColor="#38BDF8" android:pathData="M54,27 L56,33 L62,35 L56,37 L54,43 L52,37 L46,35 L52,33 Z"/>
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
        <activity android:name=".SettingsActivity" android:exported="false" />
        <activity android:name=".WidgetConfigActivity" android:exported="true" android:label="Widget Setup">
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

"app/src/main/java/ir/nimasirex/aistatus/AppConfig.java": """package ir.nimasirex.aistatus;
import android.content.Context;
import android.content.SharedPreferences;
import android.content.res.Configuration;
import android.graphics.Color;
import android.graphics.drawable.GradientDrawable;
import android.view.Gravity;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;
import java.util.*;

public class AppConfig {
    public static final String PREFS = "AIPrefs";
    public static final String VERSION_STR = "1.6.0 (Build 8)";

    public static boolean isFa(Context c) {
        return c.getSharedPreferences(PREFS, Context.MODE_PRIVATE).getString("lang", "fa").equals("fa");
    }

    public static void setLang(Context c, String lang) {
        c.getSharedPreferences(PREFS, Context.MODE_PRIVATE).edit().putString("lang", lang).apply();
    }

    // Theme: 0 = Auto (System), 1 = Light (Day), 2 = Dark (Night)
    public static int getThemeMode(Context c) {
        return c.getSharedPreferences(PREFS, Context.MODE_PRIVATE).getInt("theme_mode", 2);
    }

    public static void setThemeMode(Context c, int mode) {
        c.getSharedPreferences(PREFS, Context.MODE_PRIVATE).edit().putInt("theme_mode", mode).apply();
    }

    public static boolean isDark(Context c) {
        int mode = getThemeMode(c);
        if (mode == 1) return false;
        if (mode == 2) return true;
        int ui = c.getResources().getConfiguration().uiMode & Configuration.UI_MODE_NIGHT_MASK;
        return ui == Configuration.UI_MODE_NIGHT_YES;
    }

    public static boolean getDefaultDeepTest(Context c) {
        return c.getSharedPreferences(PREFS, Context.MODE_PRIVATE).getBoolean("default_deep", true);
    }

    public static void setDefaultDeepTest(Context c, boolean deep) {
        c.getSharedPreferences(PREFS, Context.MODE_PRIVATE).edit().putBoolean("default_deep", deep).apply();
    }

    // Multi API Key Manager
    public static List<String> getApiKeys(Context c) {
        SharedPreferences p = c.getSharedPreferences(PREFS, Context.MODE_PRIVATE);
        String raw = p.getString("api_keys_list", "");
        List<String> list = new ArrayList<>();
        if (!raw.isEmpty()) {
            for (String s : raw.split(";;;")) {
                if (!s.trim().isEmpty() && !list.contains(s.trim())) list.add(s.trim());
            }
        }
        String legacy = p.getString("gemini_api_key", "").trim();
        if (!legacy.isEmpty() && !list.contains(legacy)) {
            list.add(legacy);
            saveApiKeys(c, list);
        }
        return list;
    }

    public static void saveApiKeys(Context c, List<String> keys) {
        StringBuilder sb = new StringBuilder();
        for (String k : keys) {
            if (!k.trim().isEmpty()) {
                if (sb.length() > 0) sb.append(";;;");
                sb.append(k.trim());
            }
        }
        c.getSharedPreferences(PREFS, Context.MODE_PRIVATE).edit().putString("api_keys_list", sb.toString()).apply();
    }

    public static String getActiveApiKey(Context c) {
        return c.getSharedPreferences(PREFS, Context.MODE_PRIVATE).getString("active_api_key", "").trim();
    }

    public static void setActiveApiKey(Context c, String key) {
        c.getSharedPreferences(PREFS, Context.MODE_PRIVATE).edit()
            .putString("active_api_key", key.trim())
            .putString("gemini_api_key", key.trim())
            .apply();
    }

    public static String maskKey(String k, int index, boolean fa) {
        if (k == null || k.isEmpty()) return fa ? "بدون کلید (تست عمومی)" : "No Key (Public Check)";
        String shortK = k.length() > 10 ? k.substring(0, 5) + "..." + k.substring(k.length() - 4) : k;
        return (fa ? "کلید #" : "Key #") + index + " (" + shortK + ")";
    }

    // Service visibility filter
    public static Set<String> getDisabledServices(Context c) {
        return new HashSet<>(c.getSharedPreferences(PREFS, Context.MODE_PRIVATE).getStringSet("disabled_services", new HashSet<>()));
    }

    public static void setDisabledServices(Context c, Set<String> disabled) {
        c.getSharedPreferences(PREFS, Context.MODE_PRIVATE).edit().putStringSet("disabled_services", disabled).apply();
    }

    public static boolean isServiceEnabled(Context c, String id) {
        return !getDisabledServices(c).contains(id);
    }

    // Theme Colors
    public static int bgPage(Context c) { return Color.parseColor(isDark(c) ? "#0B1120" : "#F1F5F9"); }
    public static int bgCard(Context c) { return Color.parseColor(isDark(c) ? "#1E293B" : "#FFFFFF"); }
    public static int bgToolbar(Context c) { return Color.parseColor(isDark(c) ? "#1E293B" : "#0284C7"); }
    public static int strokeCard(Context c) { return Color.parseColor(isDark(c) ? "#334155" : "#CBD5E1"); }
    public static int strokeAccent(Context c) { return Color.parseColor(isDark(c) ? "#38BDF8" : "#0284C7"); }
    public static int textPrimary(Context c) { return Color.parseColor(isDark(c) ? "#F8FAFC" : "#0F172A"); }
    public static int textSecondary(Context c) { return Color.parseColor(isDark(c) ? "#94A3B8" : "#475569"); }
    public static int textAccent(Context c) { return Color.parseColor(isDark(c) ? "#38BDF8" : "#0284C7"); }

    public static GradientDrawable makeCard(int bgColor, int strokeColor, int radius) {
        GradientDrawable gd = new GradientDrawable();
        gd.setColor(bgColor);
        gd.setCornerRadius(radius);
        if (strokeColor != 0) gd.setStroke(2, strokeColor);
        return gd;
    }

    public static void showStylishBanner(Context c, String msg) {
        Toast t = Toast.makeText(c, msg, Toast.LENGTH_LONG);
        t.show();
    }
}
""",

"app/src/main/java/ir/nimasirex/aistatus/ServiceData.java": """package ir.nimasirex.aistatus;
import android.content.Context;
import java.io.*;
import java.net.*;
import java.util.*;

public class ServiceData {
    public static class AIService {
        public String id, name, url;
        public int catIndex;
        public boolean supportsApiKey;
        public AIService(String id, int catIndex, String n, String u, boolean k) {
            this.id = id; this.catIndex = catIndex; this.name = n; this.url = u; this.supportsApiKey = k;
        }
    }

    public static final String[] CATEGORIES_FA = {
        "خانواده گوگل و جمینای (Google & Gemini)",
        "خانواده اوپن‌ای‌آی (OpenAI / ChatGPT)",
        "خانواده آنتروپیک (Anthropic / Claude)",
        "خانواده پرپلکسیتی (Perplexity AI)",
        "خانواده مایکروسافت و گیت‌هاب (Copilot)",
        "خانواده ایکس و متا (Grok & Meta AI)",
        "پلتفرم‌های ابزار و مدل‌های مکمل"
    };

    public static final String[] CATEGORIES_EN = {
        "Google & Gemini Family",
        "OpenAI / ChatGPT Family",
        "Anthropic / Claude Family",
        "Perplexity AI Family",
        "Microsoft & GitHub Copilot",
        "xAI Grok & Meta AI",
        "AI Tools & Cloud Platforms"
    };

    public static String getCategoryTitle(Context c, int idx) {
        return AppConfig.isFa(c) ? CATEGORIES_FA[idx] : CATEGORIES_EN[idx];
    }

    public static List<AIService> getAllServices() {
        List<AIService> l = new ArrayList<>();
        l.add(new AIService("gem_web", 0, "Gemini Web/App", "https://gemini.google.com/app", false));
        l.add(new AIService("ai_studio", 0, "Google AI Studio", "https://aistudio.google.com", false));
        l.add(new AIService("gem_api", 0, "Gemini API", "https://generativelanguage.googleapis.com/v1beta/models", true));
        l.add(new AIService("notebook_lm", 0, "NotebookLM", "https://notebooklm.google.com", false));
        l.add(new AIService("google_labs", 0, "Google Labs", "https://labs.google/fx", false));
        l.add(new AIService("vertex_ai", 0, "Vertex AI", "https://console.cloud.google.com/vertex-ai", false));
        l.add(new AIService("chatgpt_web", 1, "ChatGPT Web/App", "https://chatgpt.com", false));
        l.add(new AIService("openai_plat", 1, "OpenAI Platform", "https://platform.openai.com", false));
        l.add(new AIService("openai_api", 1, "OpenAI API", "https://api.openai.com/v1/models", false));
        l.add(new AIService("sora", 1, "Sora Video AI", "https://sora.com", false));
        l.add(new AIService("claude_web", 2, "Claude Web/App", "https://claude.ai", false));
        l.add(new AIService("claude_con", 2, "Anthropic Console", "https://console.anthropic.com", false));
        l.add(new AIService("claude_api", 2, "Claude API", "https://api.anthropic.com/v1/messages", false));
        l.add(new AIService("perp_web", 3, "Perplexity Web", "https://www.perplexity.ai", false));
        l.add(new AIService("perp_api", 3, "Perplexity API", "https://api.perplexity.ai", false));
        l.add(new AIService("ms_copilot", 4, "Microsoft Copilot", "https://copilot.microsoft.com", false));
        l.add(new AIService("gh_copilot", 4, "GitHub Copilot", "https://api.githubcopilot.com/_ping", false));
        l.add(new AIService("grok_ai", 5, "Grok (xAI)", "https://grok.com", false));
        l.add(new AIService("meta_ai", 5, "Meta AI (Llama)", "https://www.meta.ai", false));
        l.add(new AIService("deepseek", 6, "DeepSeek Chat", "https://chat.deepseek.com", false));
        l.add(new AIService("huggingface", 6, "Hugging Face", "https://huggingface.co", false));
        l.add(new AIService("elevenlabs", 6, "ElevenLabs Audio", "https://api.elevenlabs.io/v1/voices", false));
        l.add(new AIService("replicate", 6, "Replicate Cloud", "https://api.replicate.com/v1/models", false));
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

    public static String checkService(Context ctx, AIService s, boolean isDeepTest) {
        boolean fa = AppConfig.isFa(ctx);
        String key = AppConfig.getActiveApiKey(ctx);
        long t0 = System.currentTimeMillis();
        try {
            String targetUrl = s.url;
            if (s.supportsApiKey && !key.isEmpty()) {
                targetUrl = "https://generativelanguage.googleapis.com/v1beta/models?key=" + key;
            } else if (isDeepTest && s.id.equals("chatgpt_web")) {
                targetUrl = "https://chatgpt.com/backend-api/models";
            }

            HttpURLConnection c = (HttpURLConnection) new URL(targetUrl).openConnection();
            c.setConnectTimeout(6000); c.setReadTimeout(6000); c.setInstanceFollowRedirects(true);
            c.setRequestProperty("User-Agent", "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36");

            int code = c.getResponseCode();
            String snip = readStream(code >= 400 ? c.getErrorStream() : c.getInputStream());
            String fu = c.getURL().toString().toLowerCase();

            if (isDeepTest && s.catIndex == 0 && !s.id.equals("vertex_ai")) {
                if (isGoogleAiGeoBlocked()) {
                    long ping = System.currentTimeMillis() - t0;
                    return (fa ? "🟡 تحریم آی‌پی (" : "🟡 Geo-Blocked (") + ping + "ms)";
                }
            }

            long ping = System.currentTimeMillis() - t0;

            if (fu.contains("unsupported") || fu.contains("region") || fu.contains("faq") || fu.contains("unavailable") ||
                snip.contains("country isn't supported") ||
                snip.contains("location is not supported") ||
                snip.contains("not available in your country") ||
                snip.contains("unsupported_country") ||
                snip.contains("region_not_supported") ||
                snip.contains("error 1020")) {
                return (fa ? "🟡 تحریم آی‌پی (" : "🟡 Geo-Blocked (") + ping + "ms)";
            }

            if (s.supportsApiKey && key.isEmpty() && (code == 403 || code == 400)) {
                return (fa ? "🟢 درگاه باز (" : "🟢 Port Open (") + ping + "ms)";
            }

            if (code == 403 || code == 451) {
                if (!isDeepTest && (s.catIndex == 1 || s.catIndex == 2 || s.catIndex == 3)) {
                    return (fa ? "🟢 در دسترس (" : "🟢 Reachable (") + ping + "ms)";
                }
                return (fa ? "🟡 محدودیت آی‌پی (" : "🟡 Restricted (") + ping + "ms)";
            }

            if (s.supportsApiKey && !key.isEmpty() && code == 200) {
                return (fa ? "🟢 متصل با کلید (" : "🟢 Key Valid (") + ping + "ms)";
            }

            if ((code >= 200 && code < 400) || code == 401 || code == 400 || code == 405) {
                return (fa ? "🟢 متصل (" : "🟢 Connected (") + ping + "ms)";
            }
            return (fa ? "🟡 کد " : "🟡 Code ") + code + " (" + ping + "ms)";
        } catch (Exception e) {
            return fa ? "🔴 قطع / عدم دسترسی" : "🔴 Offline / Blocked";
        }
    }
}
""",

"app/src/main/java/ir/nimasirex/aistatus/MainActivity.java": """package ir.nimasirex.aistatus;
import android.app.AlertDialog;
import android.content.*;
import android.graphics.*;
import android.os.Bundle;
import android.view.*;
import android.widget.*;
import androidx.appcompat.app.AppCompatActivity;
import androidx.drawerlayout.widget.DrawerLayout;
import java.util.*;
import java.util.concurrent.*;

public class MainActivity extends AppCompatActivity {
    private DrawerLayout drawerLayout;
    private LinearLayout drawerPanel;
    private final List<CheckBox> catBoxes = new ArrayList<>();
    private final Map<String, TextView> resViews = new HashMap<>();
    private LinearLayout resBox;
    private Switch deepSwitch;
    private Spinner mainKeySpinner;
    private final ExecutorService exec = Executors.newFixedThreadPool(6);
    private String lastConfigSig = "";

    @Override protected void onCreate(Bundle b) {
        super.onCreate(b);
        lastConfigSig = getConfigSig();
        buildUi();
    }

    @Override protected void onResume() {
        super.onResume();
        String curSig = getConfigSig();
        if (!curSig.equals(lastConfigSig)) {
            lastConfigSig = curSig;
            buildUi();
        }
    }

    private String getConfigSig() {
        return AppConfig.isFa(this) + "_" + AppConfig.getThemeMode(this) + "_" +
               AppConfig.getDefaultDeepTest(this) + "_" + AppConfig.getActiveApiKey(this) + "_" +
               AppConfig.getApiKeys(this).size() + "_" + AppConfig.getDisabledServices(this).toString();
    }

    private void buildUi() {
        boolean fa = AppConfig.isFa(this);
        int dir = fa ? View.LAYOUT_DIRECTION_RTL : View.LAYOUT_DIRECTION_LTR;
        int drawerGravity = fa ? Gravity.RIGHT : Gravity.LEFT;

        drawerLayout = new DrawerLayout(this);
        drawerLayout.setLayoutDirection(dir);

        // Main Vertical Container
        LinearLayout mainContainer = new LinearLayout(this);
        mainContainer.setOrientation(LinearLayout.VERTICAL);
        mainContainer.setBackgroundColor(AppConfig.bgPage(this));
        mainContainer.setLayoutDirection(dir);

        // Custom Top Toolbar with Hamburger Icon
        LinearLayout toolbar = new LinearLayout(this);
        toolbar.setOrientation(LinearLayout.HORIZONTAL);
        toolbar.setGravity(Gravity.CENTER_VERTICAL);
        toolbar.setPadding(28, 36, 28, 36);
        toolbar.setBackgroundColor(AppConfig.bgToolbar(this));

        TextView menuBtn = new TextView(this);
        menuBtn.setText("☰");
        menuBtn.setTextColor(Color.WHITE);
        menuBtn.setTextSize(24);
        menuBtn.setPadding(20, 4, 20, 4);
        menuBtn.setOnClickListener(v -> {
            if (drawerLayout.isDrawerOpen(drawerGravity)) drawerLayout.closeDrawer(drawerGravity);
            else drawerLayout.openDrawer(drawerGravity);
        });

        TextView titleTv = new TextView(this);
        titleTv.setText(fa ? "⚡ رادار هوش مصنوعی" : "⚡ AI Status & Ping");
        titleTv.setTextColor(Color.WHITE);
        titleTv.setTextSize(18);
        titleTv.setTypeface(null, Typeface.BOLD);
        titleTv.setPadding(16, 0, 16, 0);
        titleTv.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1f));

        TextView gearBtn = new TextView(this);
        gearBtn.setText("⚙️");
        gearBtn.setTextSize(20);
        gearBtn.setPadding(16, 4, 16, 4);
        gearBtn.setOnClickListener(v -> startActivity(new Intent(this, SettingsActivity.class)));

        toolbar.addView(menuBtn);
        toolbar.addView(titleTv);
        toolbar.addView(gearBtn);
        mainContainer.addView(toolbar, new LinearLayout.LayoutParams(-1, -2));

        // Scrollable Content
        ScrollView sv = new ScrollView(this);
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(36, 36, 36, 60);
        root.setLayoutDirection(dir);
        sv.addView(root);
        mainContainer.addView(sv, new LinearLayout.LayoutParams(-1, -1, 1f));

        // 1. Header Card
        LinearLayout headerCard = new LinearLayout(this);
        headerCard.setOrientation(LinearLayout.VERTICAL);
        headerCard.setPadding(32, 32, 32, 32);
        headerCard.setBackground(AppConfig.makeCard(AppConfig.bgCard(this), AppConfig.strokeAccent(this), 32));
        root.addView(headerCard);

        TextView h = new TextView(this);
        h.setText(fa ? "مانیتورینگ هوشمند پینگ و تحریم AI" : "Smart AI Ping & Geo-Block Radar");
        h.setTextColor(AppConfig.textAccent(this));
        h.setTextSize(17);
        h.setTypeface(null, Typeface.BOLD);
        h.setGravity(Gravity.CENTER);
        headerCard.addView(h);

        TextView sub = new TextView(this);
        sub.setText(fa ? "بررسی لحظه‌ای اتصال سرورها با قابلیت تشخیص تحریم" : "Real-time connectivity & restriction diagnostics");
        sub.setTextColor(AppConfig.textSecondary(this));
        sub.setTextSize(12);
        sub.setGravity(Gravity.CENTER);
        sub.setPadding(0, 8, 0, 20);
        headerCard.addView(sub);

        Button wBtn = new Button(this);
        wBtn.setText(fa ? "➕ تنظیم و افزودن ویجت به صفحه اصلی" : "➕ Configure & Add Home Screen Widget");
        wBtn.setTextColor(Color.WHITE);
        wBtn.setTypeface(null, Typeface.BOLD);
        wBtn.setBackground(AppConfig.makeCard(Color.parseColor("#059669"), 0, 24));
        headerCard.addView(wBtn);
        wBtn.setOnClickListener(v -> startActivity(new Intent(this, WidgetConfigActivity.class)));

        // 2. Test Mode Card (Shallow vs Deep + Info Button)
        LinearLayout modeCard = new LinearLayout(this);
        modeCard.setOrientation(LinearLayout.HORIZONTAL);
        modeCard.setGravity(Gravity.CENTER_VERTICAL);
        modeCard.setPadding(28, 22, 28, 22);
        modeCard.setBackground(AppConfig.makeCard(AppConfig.bgCard(this), AppConfig.strokeCard(this), 26));
        LinearLayout.LayoutParams mp = new LinearLayout.LayoutParams(-1, -2);
        mp.setMargins(0, 24, 0, 0);
        root.addView(modeCard, mp);

        deepSwitch = new Switch(this);
        deepSwitch.setText(fa ? "حالت تست عمیق (ضد فریب)" : "Deep Test Mode (Strict)");
        deepSwitch.setTextColor(AppConfig.textPrimary(this));
        deepSwitch.setTypeface(null, Typeface.BOLD);
        deepSwitch.setChecked(AppConfig.getDefaultDeepTest(this));
        deepSwitch.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1f));
        modeCard.addView(deepSwitch);

        Button infoBtn = new Button(this);
        infoBtn.setText(fa ? "❗ راهنما" : "❗ Info");
        infoBtn.setTextColor(Color.WHITE);
        infoBtn.setTextSize(12);
        infoBtn.setBackground(AppConfig.makeCard(Color.parseColor("#0284C7"), 0, 20));
        infoBtn.setOnClickListener(v -> showTestModeInfoDialog(fa));
        modeCard.addView(infoBtn);

        // 3. Quick API Key Dropdown Card (shown if user saved keys, or link to add)
        List<String> savedKeys = AppConfig.getApiKeys(this);
        LinearLayout keyCard = new LinearLayout(this);
        keyCard.setOrientation(LinearLayout.VERTICAL);
        keyCard.setPadding(28, 22, 28, 22);
        keyCard.setBackground(AppConfig.makeCard(AppConfig.bgCard(this), AppConfig.strokeCard(this), 26));
        root.addView(keyCard, mp);

        TextView kt = new TextView(this);
        kt.setText(fa ? "🔑 کلید فعال Gemini API:" : "🔑 Active Gemini API Key:");
        kt.setTextColor(AppConfig.textSecondary(this));
        kt.setTextSize(12);
        keyCard.addView(kt);

        List<String> spinLabels = new ArrayList<>();
        final List<String> spinValues = new ArrayList<>();
        spinLabels.add(AppConfig.maskKey("", 0, fa));
        spinValues.add("");
        for (int i = 0; i < savedKeys.size(); i++) {
            spinLabels.add(AppConfig.maskKey(savedKeys.get(i), i + 1, fa));
            spinValues.add(savedKeys.get(i));
        }

        mainKeySpinner = new Spinner(this);
        ArrayAdapter<String> spinAdapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item, spinLabels);
        mainKeySpinner.setAdapter(spinAdapter);
        String activeKey = AppConfig.getActiveApiKey(this);
        int selIdx = spinValues.indexOf(activeKey);
        if (selIdx >= 0) mainKeySpinner.setSelection(selIdx);

        mainKeySpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override public void onItemSelected(AdapterView<?> p, View v, int pos, long id) {
                AppConfig.setActiveApiKey(MainActivity.this, spinValues.get(pos));
            }
            @Override public void onNothingSelected(AdapterView<?> p) {}
        });
        keyCard.addView(mainKeySpinner);

        // 4. Categories Card
        LinearLayout catCard = new LinearLayout(this);
        catCard.setOrientation(LinearLayout.VERTICAL);
        catCard.setPadding(28, 24, 28, 24);
        catCard.setBackground(AppConfig.makeCard(AppConfig.bgCard(this), AppConfig.strokeCard(this), 28));
        root.addView(catCard, mp);

        TextView sh = new TextView(this);
        sh.setText(fa ? "۱. خانواده‌های مورد نظر برای تست:" : "1. Select AI Families to Test:");
        sh.setTextColor(AppConfig.textPrimary(this));
        sh.setTypeface(null, Typeface.BOLD);
        sh.setPadding(0, 0, 0, 12);
        catCard.addView(sh);

        catBoxes.clear();
        for (int i = 0; i < ServiceData.CATEGORIES_FA.length; i++) {
            // Check if category has at least one enabled service
            boolean hasActive = false;
            for (ServiceData.AIService s : ServiceData.getAllServices()) {
                if (s.catIndex == i && AppConfig.isServiceEnabled(this, s.id)) {
                    hasActive = true; break;
                }
            }
            if (!hasActive) continue;

            CheckBox cb = new CheckBox(this);
            cb.setText(ServiceData.getCategoryTitle(this, i));
            cb.setTag(i);
            cb.setTextColor(AppConfig.textPrimary(this));
            cb.setChecked(i == 0);
            catBoxes.add(cb);
            catCard.addView(cb);
        }

        // 5. Start Test Button
        Button btn = new Button(this);
        btn.setText(fa ? "🚀 شروع تست هوشمند سرویس‌ها" : "🚀 Start Smart Diagnostic Test");
        btn.setTextColor(Color.WHITE);
        btn.setTextSize(15);
        btn.setTypeface(null, Typeface.BOLD);
        btn.setBackground(AppConfig.makeCard(Color.parseColor("#0284C7"), 0, 26));
        LinearLayout.LayoutParams bp = new LinearLayout.LayoutParams(-1, -2);
        bp.setMargins(0, 28, 0, 20);
        root.addView(btn, bp);

        resBox = new LinearLayout(this);
        resBox.setOrientation(LinearLayout.VERTICAL);
        root.addView(resBox);
        btn.setOnClickListener(v -> runTests());

        // Build Modular Navigation Drawer Panel
        drawerPanel = buildDrawerPanel(fa, dir, drawerGravity);

        drawerLayout.addView(mainContainer, new DrawerLayout.LayoutParams(-1, -1));
        DrawerLayout.LayoutParams dlp = new DrawerLayout.LayoutParams(
                (int)(getResources().getDisplayMetrics().widthPixels * 0.78), -1);
        dlp.gravity = drawerGravity;
        drawerLayout.addView(drawerPanel, dlp);

        setContentView(drawerLayout);
    }

    private LinearLayout buildDrawerPanel(boolean fa, int dir, int drawerGravity) {
        LinearLayout panel = new LinearLayout(this);
        panel.setOrientation(LinearLayout.VERTICAL);
        panel.setBackgroundColor(AppConfig.bgCard(this));
        panel.setLayoutDirection(dir);
        panel.setClickable(true);

        // Drawer Header
        LinearLayout dHead = new LinearLayout(this);
        dHead.setOrientation(LinearLayout.VERTICAL);
        dHead.setPadding(40, 72, 40, 40);
        dHead.setBackgroundColor(Color.parseColor("#0F172A"));

        TextView dhTitle = new TextView(this);
        dhTitle.setText("⚡ AI Status & Ping");
        dhTitle.setTextColor(Color.parseColor("#38BDF8"));
        dhTitle.setTextSize(20);
        dhTitle.setTypeface(null, Typeface.BOLD);
        dHead.addView(dhTitle);

        TextView dhSub = new TextView(this);
        dhSub.setText("Version " + AppConfig.VERSION_STR + "\nPowered by Gemini ✨");
        dhSub.setTextColor(Color.parseColor("#94A3B8"));
        dhSub.setTextSize(12);
        dhSub.setPadding(0, 10, 0, 0);
        dHead.addView(dhSub);
        panel.addView(dHead, new LinearLayout.LayoutParams(-1, -2));

        ScrollView dScroll = new ScrollView(this);
        LinearLayout dList = new LinearLayout(this);
        dList.setOrientation(LinearLayout.VERTICAL);
        dList.setPadding(24, 24, 24, 24);
        dScroll.addView(dList);
        panel.addView(dScroll, new LinearLayout.LayoutParams(-1, -1));

        // Section 1: Modular Categories (Expandable for future modules)
        addDrawerSectionTitle(dList, fa ? "دسته‌بندی‌های رادار" : "RADAR MODULES");

        addDrawerItem(dList, fa ? "🤖  رادار هوش مصنوعی (AI Test)" : "🤖  AI Status & Ping", true, () -> {
            drawerLayout.closeDrawer(drawerGravity);
        });

        addDrawerItem(dList, fa ? "🌐  شبکه‌های اجتماعی" : "🌐  Social Networks", false, () -> {
            drawerLayout.closeDrawer(drawerGravity);
            AppConfig.showStylishBanner(this, fa
                ? "✨ بخش رادار شبکه‌های اجتماعی به زودی در آپدیت‌های بعدی اضافه می‌شود..."
                : "✨ Social Networks Radar is coming soon in future updates...");
        });

        addDrawerItem(dList, fa ? "🎮  سرورهای بازی و گیمینگ" : "🎮  Gaming Servers", false, () -> {
            drawerLayout.closeDrawer(drawerGravity);
            AppConfig.showStylishBanner(this, fa
                ? "✨ بخش پینگ سرورهای گیمینگ به زودی اضافه می‌شود..."
                : "✨ Gaming Servers Ping is coming soon...");
        });

        // Divider
        View div = new View(this);
        div.setBackgroundColor(AppConfig.strokeCard(this));
        LinearLayout.LayoutParams dp = new LinearLayout.LayoutParams(-1, 2);
        dp.setMargins(12, 24, 12, 24);
        dList.addView(div, dp);

        // Section 2: General & App Options
        addDrawerSectionTitle(dList, fa ? "امکانات و تنظیمات" : "GENERAL & SETTINGS");

        addDrawerItem(dList, fa ? "⚙️  تنظیمات پیشرفته" : "⚙️  Settings", false, () -> {
            drawerLayout.closeDrawer(drawerGravity);
            startActivity(new Intent(this, SettingsActivity.class));
        });

        addDrawerItem(dList, fa ? "➕  تنظیم ویجت صفحه اصلی" : "➕  Widget Configuration", false, () -> {
            drawerLayout.closeDrawer(drawerGravity);
            startActivity(new Intent(this, WidgetConfigActivity.class));
        });

        addDrawerItem(dList, fa ? "ℹ️  درباره ما (About)" : "ℹ️  About Application", false, () -> {
            drawerLayout.closeDrawer(drawerGravity);
            showAboutDialog(fa);
        });

        return panel;
    }

    private void addDrawerSectionTitle(LinearLayout parent, String title) {
        TextView tv = new TextView(this);
        tv.setText(title);
        tv.setTextColor(AppConfig.textSecondary(this));
        tv.setTextSize(11);
        tv.setTypeface(null, Typeface.BOLD);
        tv.setPadding(20, 16, 20, 8);
        parent.addView(tv);
    }

    private void addDrawerItem(LinearLayout parent, String title, boolean selected, Runnable onClick) {
        TextView tv = new TextView(this);
        tv.setText(title);
        tv.setTextSize(14);
        tv.setTypeface(null, selected ? Typeface.BOLD : Typeface.NORMAL);
        tv.setTextColor(selected ? AppConfig.textAccent(this) : AppConfig.textPrimary(this));
        tv.setPadding(28, 28, 28, 28);
        if (selected) {
            tv.setBackground(AppConfig.makeCard(Color.parseColor(AppConfig.isDark(this) ? "#0F172A" : "#E0F2FE"), 0, 20));
        }
        tv.setOnClickListener(v -> onClick.run());
        parent.addView(tv);
    }

    private void showTestModeInfoDialog(boolean fa) {
        new AlertDialog.Builder(this)
            .setTitle(fa ? "تفاوت تست سطحی و تست عمیق" : "Shallow vs. Deep Test Mode")
            .setMessage(fa
                ? "🔹 تست سطحی (سریع):\nاتصال و پینگ مستقیم دامنه اصلی را بررسی می‌کند. برای سرویس‌هایی مثل ChatGPT، Claude و Perplexity که با باز شدن تونل فیلترشکن در اپلیکیشن کار می‌کنند بهترین گزینه است.\n\n🔸 تست عمیق (ضد فریب):\nعلاوه بر پینگ، به هسته مرکزی سرورها (به‌ویژه خانواده گوگل و جمینای) بسته آزمایشی می‌فرستد تا اگر صفحه اول باز بود ولی آی‌پی شما در لیست تحریم کشورها قرار داشت، فریب نخورد و تحریم را دقیق گزارش کند."
                : "🔹 Shallow Test (Fast):\nChecks direct domain reachability and ping. Ideal for apps like ChatGPT, Claude, and Perplexity.\n\n🔸 Deep Test (Strict Anti-Spoof):\nPerforms a dual-probe against core backend endpoints (especially for Google & Gemini) to detect hidden IP geo-restrictions even when the landing webpage loads.")
            .setPositiveButton(fa ? "متوجه شدم" : "Got it", null)
            .show();
    }

    private void showAboutDialog(boolean fa) {
        new AlertDialog.Builder(this)
            .setTitle(fa ? "ℹ️ درباره برنامه (About)" : "ℹ️ About AI Status & Ping")
            .setMessage(fa
                ? "⚡ نام برنامه: AI Status & Ping\n" +
                  "📦 نسخه: Version " + AppConfig.VERSION_STR + "\n\n" +
                  "👨‍💻 طراح و توسعه‌دهنده:\n" +
                  "نیما جعفری (Nima Jafari)\n\n" +
                  "🤖 موتور هوشمند و همکار توسعه:\n" +
                  "Powered by Gemini ✨\n\n" +
                  "جامع‌ترین ابزار تشخیص وضعیت اتصال، پینگ لحظه‌ای و بررسی دقیق تحریم آی‌پی برای سرویس‌های هوش مصنوعی همراه با ویجت اختصاصی."
                : "⚡ Application: AI Status & Ping\n" +
                  "📦 Version: " + AppConfig.VERSION_STR + "\n\n" +
                  "👨‍💻 Designed & Developed by:\n" +
                  "Nima Jafari (نیما جعفری)\n\n" +
                  "🤖 AI Engine & Co-Developer:\n" +
                  "Powered by Gemini ✨\n\n" +
                  "Comprehensive diagnostic radar for monitoring connectivity, real-time latency, and geo-restrictions across AI platforms.")
            .setPositiveButton(fa ? "بستن" : "Close", null)
            .show();
    }

    private void runTests() {
        boolean fa = AppConfig.isFa(this);
        resBox.removeAllViews(); resViews.clear();
        List<Integer> selCats = new ArrayList<>();
        for (CheckBox cb : catBoxes) if (cb.isChecked()) selCats.add((Integer) cb.getTag());
        if (selCats.isEmpty()) {
            Toast.makeText(this, fa ? "حداقل یک خانواده را انتخاب کنید" : "Please select at least one family", Toast.LENGTH_SHORT).show();
            return;
        }

        boolean isDeep = deepSwitch.isChecked();

        for (int catIdx : selCats) {
            TextView ch = new TextView(this);
            ch.setText("▪ " + ServiceData.getCategoryTitle(this, catIdx));
            ch.setTextColor(AppConfig.textAccent(this));
            ch.setTypeface(null, Typeface.BOLD);
            ch.setPadding(8, 24, 8, 12);
            resBox.addView(ch);

            for (ServiceData.AIService s : ServiceData.getAllServices()) {
                if (s.catIndex == catIdx && AppConfig.isServiceEnabled(this, s.id)) {
                    LinearLayout row = new LinearLayout(this);
                    row.setPadding(28, 22, 28, 22);
                    row.setGravity(Gravity.CENTER_VERTICAL);
                    row.setBackground(AppConfig.makeCard(AppConfig.bgCard(this), AppConfig.strokeCard(this), 20));
                    LinearLayout.LayoutParams rp = new LinearLayout.LayoutParams(-1, -2);
                    rp.setMargins(0, 0, 0, 14);

                    TextView nt = new TextView(this);
                    nt.setText(s.name);
                    nt.setTextColor(AppConfig.textPrimary(this));
                    nt.setTypeface(null, Typeface.BOLD);
                    nt.setTextSize(13);
                    nt.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1f));

                    TextView st = new TextView(this);
                    st.setText(fa ? "⏳ در حال تست..." : "⏳ Testing...");
                    st.setTextColor(Color.parseColor("#EAB308"));
                    st.setTextSize(12);

                    row.addView(nt);
                    row.addView(st);
                    resBox.addView(row, rp);
                    resViews.put(s.id, st);

                    exec.execute(() -> {
                        String r = ServiceData.checkService(MainActivity.this, s, isDeep);
                        runOnUiThread(() -> {
                            TextView tv = resViews.get(s.id);
                            if (tv != null) {
                                tv.setText(r);
                                tv.setTextColor(r.startsWith("🟢") ? Color.parseColor("#10B981") : r.startsWith("🟡") ? Color.parseColor("#F59E0B") : Color.parseColor("#EF4444"));
                            }
                        });
                    });
                }
            }
        }
    }
}
""",

"app/src/main/java/ir/nimasirex/aistatus/SettingsActivity.java": """package ir.nimasirex.aistatus;
import android.content.*;
import android.graphics.*;
import android.os.Bundle;
import android.view.*;
import android.widget.*;
import androidx.appcompat.app.AppCompatActivity;
import java.util.*;

public class SettingsActivity extends AppCompatActivity {
    private final List<CheckBox> serviceBoxes = new ArrayList<>();
    private Spinner keySpinner;
    private EditText newKeyInput;

    @Override protected void onCreate(Bundle b) {
        super.onCreate(b);
        buildSettingsUi();
    }

    private void buildSettingsUi() {
        boolean fa = AppConfig.isFa(this);
        int dir = fa ? View.LAYOUT_DIRECTION_RTL : View.LAYOUT_DIRECTION_LTR;

        LinearLayout main = new LinearLayout(this);
        main.setOrientation(LinearLayout.VERTICAL);
        main.setBackgroundColor(AppConfig.bgPage(this));
        main.setLayoutDirection(dir);

        // Top Bar
        LinearLayout topBar = new LinearLayout(this);
        topBar.setOrientation(LinearLayout.HORIZONTAL);
        topBar.setGravity(Gravity.CENTER_VERTICAL);
        topBar.setPadding(28, 36, 28, 36);
        topBar.setBackgroundColor(AppConfig.bgToolbar(this));

        TextView backBtn = new TextView(this);
        backBtn.setText(fa ? "➔" : "⬅");
        backBtn.setTextColor(Color.WHITE);
        backBtn.setTextSize(22);
        backBtn.setPadding(20, 4, 20, 4);
        backBtn.setOnClickListener(v -> finish());

        TextView title = new TextView(this);
        title.setText(fa ? "⚙️ تنظیمات پیشرفته برنامه" : "⚙️ Application Settings");
        title.setTextColor(Color.WHITE);
        title.setTextSize(18);
        title.setTypeface(null, Typeface.BOLD);
        title.setPadding(16, 0, 16, 0);

        topBar.addView(backBtn);
        topBar.addView(title);
        main.addView(topBar, new LinearLayout.LayoutParams(-1, -2));

        ScrollView sv = new ScrollView(this);
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(36, 36, 36, 60);
        root.setLayoutDirection(dir);
        sv.addView(root);
        main.addView(sv, new LinearLayout.LayoutParams(-1, -1));

        LinearLayout.LayoutParams cardLp = new LinearLayout.LayoutParams(-1, -2);
        cardLp.setMargins(0, 0, 0, 28);

        // 1. Language Card
        LinearLayout langCard = makeSectionCard(fa ? "🌐 زبان و جهت برنامه (Language)" : "🌐 App Language & Direction");
        RadioGroup langGroup = new RadioGroup(this);
        langGroup.setOrientation(RadioGroup.HORIZONTAL);

        RadioButton rbFa = new RadioButton(this);
        rbFa.setText("🇮🇷 فارسی (راست‌چین)");
        rbFa.setTextColor(AppConfig.textPrimary(this));
        rbFa.setChecked(fa);

        RadioButton rbEn = new RadioButton(this);
        rbEn.setText("🇬🇧 English (LTR)");
        rbEn.setTextColor(AppConfig.textPrimary(this));
        rbEn.setChecked(!fa);

        langGroup.addView(rbFa);
        langGroup.addView(rbEn);
        langCard.addView(langGroup);
        root.addView(langCard, cardLp);

        rbFa.setOnClickListener(v -> { if (!fa) { AppConfig.setLang(this, "fa"); buildSettingsUi(); } });
        rbEn.setOnClickListener(v -> { if (fa) { AppConfig.setLang(this, "en"); buildSettingsUi(); } });

        // 2. Theme Mode Card (Day / Night / System Auto)
        LinearLayout themeCard = makeSectionCard(fa ? "🌓 حالت نمایش روز و شب (Theme)" : "🌓 Appearance & Theme Mode");
        RadioGroup themeGroup = new RadioGroup(this);
        int curTheme = AppConfig.getThemeMode(this);

        RadioButton rbAuto = new RadioButton(this);
        rbAuto.setText(fa ? "📱 اتوماتیک بر اساس تنظیمات دستگاه" : "📱 System Default (Auto)");
        rbAuto.setTextColor(AppConfig.textPrimary(this));
        rbAuto.setChecked(curTheme == 0);

        RadioButton rbDay = new RadioButton(this);
        rbDay.setText(fa ? "☀️ حالت روز (پوسته روشن)" : "☀️ Day Mode (Light)");
        rbDay.setTextColor(AppConfig.textPrimary(this));
        rbDay.setChecked(curTheme == 1);

        RadioButton rbNight = new RadioButton(this);
        rbNight.setText(fa ? "🌙 حالت شب (پوسته تیره)" : "🌙 Night Mode (Dark)");
        rbNight.setTextColor(AppConfig.textPrimary(this));
        rbNight.setChecked(curTheme == 2);

        themeGroup.addView(rbAuto);
        themeGroup.addView(rbDay);
        themeGroup.addView(rbNight);
        themeCard.addView(themeGroup);
        root.addView(themeCard, cardLp);

        rbAuto.setOnClickListener(v -> { AppConfig.setThemeMode(this, 0); buildSettingsUi(); });
        rbDay.setOnClickListener(v -> { AppConfig.setThemeMode(this, 1); buildSettingsUi(); });
        rbNight.setOnClickListener(v -> { AppConfig.setThemeMode(this, 2); buildSettingsUi(); });

        // 3. Default Test Mode Card
        LinearLayout testCard = makeSectionCard(fa ? "⚡ حالت پیش‌فرض تست (Default Test Mode)" : "⚡ Default Diagnostic Mode");
        Switch defDeep = new Switch(this);
        defDeep.setText(fa ? "شروع برنامه با «تست عمیق (ضد فریب)»" : "Start with Deep Test Mode enabled");
        defDeep.setTextColor(AppConfig.textPrimary(this));
        defDeep.setChecked(AppConfig.getDefaultDeepTest(this));
        defDeep.setOnCheckedChangeListener((bView, checked) -> AppConfig.setDefaultDeepTest(this, checked));
        testCard.addView(defDeep);
        root.addView(testCard, cardLp);

        // 4. Multi API Key Manager Card (Auto-Add & Dropdown)
        LinearLayout apiCard = makeSectionCard(fa ? "🔑 مدیریت کلیدهای Gemini API" : "🔑 Gemini API Keys Manager");

        TextView apiSub = new TextView(this);
        apiSub.setText(fa ? "کلید جدید را وارد کنید تا خودکار به لیست کشویی اضافه شود:" : "Add a new key to automatically include it in the dropdown:");
        apiSub.setTextColor(AppConfig.textSecondary(this));
        apiSub.setTextSize(12);
        apiCard.addView(apiSub);

        LinearLayout addRow = new LinearLayout(this);
        addRow.setOrientation(LinearLayout.HORIZONTAL);
        addRow.setGravity(Gravity.CENTER_VERTICAL);
        addRow.setPadding(0, 12, 0, 16);

        newKeyInput = new EditText(this);
        newKeyInput.setHint(fa ? "کلید AIzaSy... را اینجا پیست کنید" : "Paste AIzaSy... key here");
        newKeyInput.setHintTextColor(AppConfig.textSecondary(this));
        newKeyInput.setTextColor(AppConfig.textPrimary(this));
        newKeyInput.setTextSize(13);
        newKeyInput.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1f));

        Button addKeyBtn = new Button(this);
        addKeyBtn.setText(fa ? "➕ افزودن" : "➕ Add");
        addKeyBtn.setTextColor(Color.WHITE);
        addKeyBtn.setBackground(AppConfig.makeCard(Color.parseColor("#059669"), 0, 18));

        addRow.addView(newKeyInput);
        addRow.addView(addKeyBtn);
        apiCard.addView(addRow);

        TextView dropLabel = new TextView(this);
        dropLabel.setText(fa ? "انتخاب کلید فعال از لیست کشویی:" : "Select Active Key from Dropdown:");
        dropLabel.setTextColor(AppConfig.textPrimary(this));
        dropLabel.setTextSize(13);
        apiCard.addView(dropLabel);

        LinearLayout spinRow = new LinearLayout(this);
        spinRow.setOrientation(LinearLayout.HORIZONTAL);
        spinRow.setGravity(Gravity.CENTER_VERTICAL);
        spinRow.setPadding(0, 8, 0, 0);

        keySpinner = new Spinner(this);
        keySpinner.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1f));

        Button delKeyBtn = new Button(this);
        delKeyBtn.setText("🗑️");
        delKeyBtn.setTextColor(Color.WHITE);
        delKeyBtn.setBackground(AppConfig.makeCard(Color.parseColor("#EF4444"), 0, 18));

        spinRow.addView(keySpinner);
        spinRow.addView(delKeyBtn);
        apiCard.addView(spinRow);
        root.addView(apiCard, cardLp);

        refreshKeySpinner(fa);

        addKeyBtn.setOnClickListener(v -> {
            String k = newKeyInput.getText().toString().trim();
            if (k.isEmpty()) {
                Toast.makeText(this, fa ? "لطفاً ابتدا کلید را وارد کنید" : "Please enter a key first", Toast.LENGTH_SHORT).show();
                return;
            }
            List<String> keys = AppConfig.getApiKeys(this);
            if (!keys.contains(k)) keys.add(k);
            AppConfig.saveApiKeys(this, keys);
            AppConfig.setActiveApiKey(this, k);
            newKeyInput.setText("");
            refreshKeySpinner(fa);
            Toast.makeText(this, fa ? "✅ کلید اضافه و فعال شد!" : "✅ Key added and selected!", Toast.LENGTH_SHORT).show();
        });

        delKeyBtn.setOnClickListener(v -> {
            String active = AppConfig.getActiveApiKey(this);
            if (active.isEmpty()) {
                Toast.makeText(this, fa ? "کلیدی برای حذف انتخاب نشده است" : "No key selected to delete", Toast.LENGTH_SHORT).show();
                return;
            }
            List<String> keys = AppConfig.getApiKeys(this);
            keys.remove(active);
            AppConfig.saveApiKeys(this, keys);
            AppConfig.setActiveApiKey(this, keys.isEmpty() ? "" : keys.get(0));
            refreshKeySpinner(fa);
            Toast.makeText(this, fa ? "🗑️ کلید انتخابی حذف شد" : "🗑️ Selected key removed", Toast.LENGTH_SHORT).show();
        });

        // 5. Manage Visible Services Card
        LinearLayout srvCard = makeSectionCard(fa ? "🎛️ مدیریت نمایش سرویس‌ها در صفحه اصلی" : "🎛️ Manage Visible AI Services");
        TextView srvHint = new TextView(this);
        srvHint.setText(fa
            ? "هر سرویسی را که تیکش را بردارید، دیگر در صفحه اصلی و ویجت نمایش داده نمی‌شود:"
            : "Uncheck any service you don't use to hide it from the dashboard:");
        srvHint.setTextColor(AppConfig.textSecondary(this));
        srvHint.setTextSize(12);
        srvHint.setPadding(0, 0, 0, 12);
        srvCard.addView(srvHint);

        Set<String> disabled = AppConfig.getDisabledServices(this);
        serviceBoxes.clear();
        int curCat = -1;
        for (ServiceData.AIService s : ServiceData.getAllServices()) {
            if (s.catIndex != curCat) {
                curCat = s.catIndex;
                TextView ct = new TextView(this);
                ct.setText("▪ " + ServiceData.getCategoryTitle(this, curCat));
                ct.setTextColor(AppConfig.textAccent(this));
                ct.setTypeface(null, Typeface.BOLD);
                ct.setPadding(0, 16, 0, 4);
                srvCard.addView(ct);
            }
            CheckBox cb = new CheckBox(this);
            cb.setText(s.name);
            cb.setTag(s.id);
            cb.setTextColor(AppConfig.textPrimary(this));
            cb.setChecked(!disabled.contains(s.id));
            cb.setOnCheckedChangeListener((bv, isChecked) -> saveServiceVisibility());
            serviceBoxes.add(cb);
            srvCard.addView(cb);
        }
        root.addView(srvCard, cardLp);

        Button doneBtn = new Button(this);
        doneBtn.setText(fa ? "✅ ذخیره و بازگشت به صفحه اصلی" : "✅ Save & Return to Dashboard");
        doneBtn.setTextColor(Color.WHITE);
        doneBtn.setTypeface(null, Typeface.BOLD);
        doneBtn.setBackground(AppConfig.makeCard(Color.parseColor("#0284C7"), 0, 24));
        doneBtn.setOnClickListener(v -> finish());
        root.addView(doneBtn);

        setContentView(main);
    }

    private LinearLayout makeSectionCard(String titleText) {
        LinearLayout card = new LinearLayout(this);
        card.setOrientation(LinearLayout.VERTICAL);
        card.setPadding(28, 26, 28, 26);
        card.setBackground(AppConfig.makeCard(AppConfig.bgCard(this), AppConfig.strokeCard(this), 28));

        TextView t = new TextView(this);
        t.setText(titleText);
        t.setTextColor(AppConfig.textAccent(this));
        t.setTextSize(15);
        t.setTypeface(null, Typeface.BOLD);
        t.setPadding(0, 0, 0, 14);
        card.addView(t);
        return card;
    }

    private void refreshKeySpinner(boolean fa) {
        List<String> keys = AppConfig.getApiKeys(this);
        List<String> labels = new ArrayList<>();
        final List<String> values = new ArrayList<>();

        labels.add(AppConfig.maskKey("", 0, fa));
        values.add("");

        for (int i = 0; i < keys.size(); i++) {
            labels.add(AppConfig.maskKey(keys.get(i), i + 1, fa));
            values.add(keys.get(i));
        }

        ArrayAdapter<String> ad = new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item, labels);
        keySpinner.setAdapter(ad);

        String active = AppConfig.getActiveApiKey(this);
        int idx = values.indexOf(active);
        if (idx >= 0) keySpinner.setSelection(idx);

        keySpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override public void onItemSelected(AdapterView<?> p, View v, int pos, long id) {
                AppConfig.setActiveApiKey(SettingsActivity.this, values.get(pos));
            }
            @Override public void onNothingSelected(AdapterView<?> p) {}
        });
    }

    private void saveServiceVisibility() {
        Set<String> dis = new HashSet<>();
        for (CheckBox cb : serviceBoxes) {
            if (!cb.isChecked()) dis.add((String) cb.getTag());
        }
        AppConfig.setDisabledServices(this, dis);
    }
}
""",

"app/src/main/java/ir/nimasirex/aistatus/WidgetConfigActivity.java": """package ir.nimasirex.aistatus;
import android.appwidget.AppWidgetManager;
import android.content.*;
import android.graphics.*;
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

        boolean fa = AppConfig.isFa(this);
        int dir = fa ? View.LAYOUT_DIRECTION_RTL : View.LAYOUT_DIRECTION_LTR;

        ScrollView sv = new ScrollView(this); sv.setBackgroundColor(AppConfig.bgPage(this));
        LinearLayout root = new LinearLayout(this); root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(40, 60, 40, 60); root.setLayoutDirection(dir); sv.addView(root);

        TextView t = new TextView(this);
        t.setText(fa ? "انتخاب سرویس‌های ویجت صفحه اصلی" : "Select Services for Home Widget");
        t.setTextColor(AppConfig.textAccent(this)); t.setTextSize(17); t.setTypeface(null, Typeface.BOLD);
        t.setPadding(0, 0, 0, 16); root.addView(t);

        Set<String> saved = getSharedPreferences("WidgetPrefs", MODE_PRIVATE).getStringSet("w_default", null);

        int cur = -1;
        for (ServiceData.AIService s : ServiceData.getAllServices()) {
            if (!AppConfig.isServiceEnabled(this, s.id)) continue;
            if (s.catIndex != cur) {
                cur = s.catIndex;
                TextView ct = new TextView(this); ct.setText("▪ " + ServiceData.getCategoryTitle(this, cur));
                ct.setTextColor(AppConfig.textAccent(this));
                ct.setTypeface(null, Typeface.BOLD); ct.setPadding(0, 22, 0, 6); root.addView(ct);
            }
            CheckBox cb = new CheckBox(this); cb.setText(s.name); cb.setTag(s.id);
            cb.setTextColor(AppConfig.textPrimary(this));
            if (saved != null) cb.setChecked(saved.contains(s.id));
            else if (s.id.equals("gem_web") || s.id.equals("chatgpt_web") || s.id.equals("grok_ai")) cb.setChecked(true);
            boxes.add(cb); root.addView(cb);
        }

        Button btn = new Button(this);
        btn.setText(fa ? "✅ ذخیره و بروزرسانی ویجت" : "✅ Save & Update Widget");
        btn.setBackground(AppConfig.makeCard(Color.parseColor("#059669"), 0, 24));
        btn.setTextColor(Color.WHITE); btn.setTypeface(null, Typeface.BOLD);
        LinearLayout.LayoutParams bp = new LinearLayout.LayoutParams(-1, -2);
        bp.setMargins(0, 32, 0, 16);
        root.addView(btn, bp);

        btn.setOnClickListener(v -> {
            Set<String> ids = new HashSet<>();
            for (CheckBox cb : boxes) if (cb.isChecked()) ids.add((String) cb.getTag());
            if (ids.isEmpty()) {
                Toast.makeText(this, fa ? "حداقل یک سرویس انتخاب کنید" : "Select at least one service", Toast.LENGTH_SHORT).show();
                return;
            }

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
                    Toast.makeText(this, fa ? "ویجت شما روی صفحه اصلی بروزرسانی شد!" : "Widget updated!", Toast.LENGTH_SHORT).show();
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
        boolean fa = AppConfig.isFa(c);
        RemoteViews v = new RemoteViews(c.getPackageName(), R.layout.widget_layout);
        v.setTextViewText(R.id.widget_title, fa ? "⚡ رادار هوش مصنوعی" : "⚡ AI Status Radar");
        v.setTextViewText(R.id.widget_refresh_hint, fa ? "🔄 بروزرسانی" : "🔄 Refresh");
        v.setTextViewText(R.id.widget_results, fa ? "⏳ در حال تست لحظه‌ای سرورها..." : "⏳ Checking servers...");
        Intent i = new Intent(c, StatusWidget.class); i.setAction(ACT); i.putExtra(AppWidgetManager.EXTRA_APPWIDGET_ID, id);
        PendingIntent pi = PendingIntent.getBroadcast(c, id, i, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        v.setOnClickPendingIntent(R.id.widget_root, pi);
        m.updateAppWidget(id, v);

        Executors.newSingleThreadExecutor().execute(() -> {
            SharedPreferences p = c.getSharedPreferences("WidgetPrefs", Context.MODE_PRIVATE);
            Set<String> ids = p.getStringSet("w_" + id, null);
            if (ids == null || ids.isEmpty()) ids = p.getStringSet("w_default", null);
            if (ids == null || ids.isEmpty()) ids = new HashSet<>(Arrays.asList("gem_web", "chatgpt_web", "grok_ai"));
            boolean isDeep = AppConfig.getDefaultDeepTest(c);
            StringBuilder sb = new StringBuilder();
            for (ServiceData.AIService s : ServiceData.getAllServices()) {
                if (ids.contains(s.id)) {
                    if (sb.length() > 0) sb.append("\\n");
                    String status = ServiceData.checkService(c, s, isDeep);
                    sb.append(status).append("  ⬅  ").append(s.name);
                }
            }
            RemoteViews uv = new RemoteViews(c.getPackageName(), R.layout.widget_layout);
            uv.setTextViewText(R.id.widget_title, fa ? "⚡ رادار هوش مصنوعی" : "⚡ AI Status Radar");
            uv.setTextViewText(R.id.widget_refresh_hint, fa ? "🔄 بروزرسانی" : "🔄 Refresh");
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
