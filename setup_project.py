import os

files = {
    "settings.gradle": """pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
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

    "app/build.gradle": """plugins {
    id 'com.android.application'
}

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

        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <activity
            android:name=".WidgetConfigActivity"
            android:exported="true"
            android:label="انتخاب سرویس‌های ویجت">
            <intent-filter>
                <action android:name="android.appwidget.action.APPWIDGET_CONFIGURE" />
            </intent-filter>
        </activity>

        <receiver
            android:name=".StatusWidget"
            android:exported="true"
            android:label="ویجت وضعیت هوش مصنوعی">
            <intent-filter>
                <action android:name="android.appwidget.action.APPWIDGET_UPDATE" />
                <action android:name="ir.nimasirex.aistatus.ACTION_REFRESH_WIDGET" />
            </intent-filter>
            <meta-data
                android:name="android.appwidget.provider"
                android:resource="@xml/widget_info" />
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
            android:text="وضعیت هوش مصنوعی"
            android:textColor="#38BDF8"
            android:textStyle="bold"
            android:textSize="13sp" />

        <TextView
            android:id="@+id/widget_refresh_hint"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="🔄 تست لحظه‌ای"
            android:textColor="#94A3B8"
            android:textSize="11sp" />
    </LinearLayout>

    <TextView
        android:id="@+id/widget_results"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:text="برای بررسی وضعیت کلیک کنید..."
        android:textColor="#F8FAFC"
        android:textSize="12sp"
        android:lineSpacingExtra="3dp" />

</LinearLayout>
""",

    "app/src/main/java/ir/nimasirex/aistatus/ServiceData.java": """package ir.nimasirex.aistatus;

import android.content.Context;
import android.content.SharedPreferences;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

public class ServiceData {

    public static class AIService {
        public String id;
        public String category;
        public String name;
        public String url;
        public boolean supportsApiKey;

        public AIService(String id, String category, String name, String url, boolean supportsApiKey) {
            this.id = id;
            this.category = category;
            this.name = name;
            this.url = url;
            this.supportsApiKey = supportsApiKey;
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
        List<AIService> list = new ArrayList<>();
        // 1. Google & Gemini
        list.add(new AIService("gem_web", CATEGORIES[0], "Gemini Web/App", "https://gemini.google.com", false));
        list.add(new AIService("ai_studio", CATEGORIES[0], "Google AI Studio", "https://aistudio.google.com", false));
        list.add(new AIService("gem_api", CATEGORIES[0], "Gemini API (مستقیم)", "https://generativelanguage.googleapis.com", true));
        list.add(new AIService("notebook_lm", CATEGORIES[0], "NotebookLM", "https://notebooklm.google.com", false));
        list.add(new AIService("google_labs", CATEGORIES[0], "Google Labs (Imagen/Veo)", "https://labs.google", false));
        list.add(new AIService("vertex_ai", CATEGORIES[0], "Vertex AI", "https://cloud.google.com/vertex-ai", false));

        // 2. OpenAI
        list.add(new AIService("chatgpt_web", CATEGORIES[1], "ChatGPT Web/App", "https://chatgpt.com", false));
        list.add(new AIService("openai_plat", CATEGORIES[1], "OpenAI Platform", "https://platform.openai.com", false));
        list.add(new AIService("openai_api", CATEGORIES[1], "OpenAI API", "https://api.openai.com", false));
        list.add(new AIService("sora", CATEGORIES[1], "Sora Video AI", "https://sora.com", false));

        // 3. Claude
        list.add(new AIService("claude_web", CATEGORIES[2], "Claude Web/App", "https://claude.ai", false));
        list.add(new AIService("claude_con", CATEGORIES[2], "Anthropic Console", "https://console.anthropic.com", false));
        list.add(new AIService("claude_api", CATEGORIES[2], "Claude API", "https://api.anthropic.com", false));

        // 4. Perplexity
        list.add(new AIService("perp_web", CATEGORIES[3], "Perplexity Web/App", "https://www.perplexity.ai", false));
        list.add(new AIService("perp_api", CATEGORIES[3], "Perplexity API", "https://api.perplexity.ai", false));

        // 5. Microsoft & GitHub
        list.add(new AIService("ms_copilot", CATEGORIES[4], "Microsoft Copilot", "https://copilot.microsoft.com", false));
        list.add(new AIService("gh_copilot", CATEGORIES[4], "GitHub Copilot", "https://github.com/features/copilot", false));

        // 6. Grok & Meta
        list.add(new AIService("grok_ai", CATEGORIES[5], "Grok (xAI)", "https://x.ai", false));
        list.add(new AIService("meta_ai", CATEGORIES[5], "Meta AI (Llama)", "https://www.meta.ai", false));

        // 7. Tools & Models
        list.add(new AIService("deepseek", CATEGORIES[6], "DeepSeek Chat", "https://chat.deepseek.com", false));
        list.add(new AIService("huggingface", CATEGORIES[6], "Hugging Face", "https://huggingface.co", false));
        list.add(new AIService("elevenlabs", CATEGORIES[6], "ElevenLabs Audio", "https://elevenlabs.io", false));
        list.add(new AIService("replicate", CATEGORIES[6], "Replicate Cloud", "https://replicate.com", false));

        return list;
    }

    public static String checkService(Context context, AIService service) {
        SharedPreferences prefs = context.getSharedPreferences("AIPrefs", Context.MODE_PRIVATE);
        String apiKey = prefs.getString("gemini_api_key", "").trim();

        long startTime = System.currentTimeMillis();
        try {
            String targetUrl = service.url;
            if (service.supportsApiKey && !apiKey.isEmpty()) {
                targetUrl = "https://generativelanguage.googleapis.com/v1beta/models?key=" + apiKey;
            }

            URL url = new URL(targetUrl);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setConnectTimeout(6500);
            conn.setReadTimeout(6500);
            conn.setInstanceFollowRedirects(true);
            conn.setRequestProperty("User-Agent", "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36");

            int code = conn.getResponseCode();
            long ping = System.currentTimeMillis() - startTime;
            String finalUrl = conn.getURL().toString().toLowerCase();

            if (finalUrl.contains("unsupported") || finalUrl.contains("region") || finalUrl.contains("faq")) {
                return "⚠️ محدودیت منطقه‌ای (آی‌پی) | " + ping + "ms";
            }

            String snippet = "";
            try {
                InputStream is = (code >= 400) ? conn.getErrorStream() : conn.getInputStream();
                if (is != null) {
                    BufferedReader reader = new BufferedReader(new InputStreamReader(is));
                    StringBuilder sb = new StringBuilder();
                    char[] buf = new char[1024];
                    int read = reader.read(buf);
                    if (read > 0) sb.append(buf, 0, read);
                    reader.close();
                    snippet = sb.toString().toLowerCase();
                }
            } catch (Exception ignored) {}

            if (code == 403 || code == 451 || snippet.contains("location is not supported") || snippet.contains("country, region, or territory not supported") || snippet.contains("unsupported_country")) {
                return "⚠️ محدودیت منطقه‌ای (403) | " + ping + "ms";
            }

            if (service.supportsApiKey && apiKey.isEmpty() && (code == 400 || code == 404 || code == 401)) {
                return "✅ درگاه باز است (" + ping + "ms)";
            }

            if (code >= 200 && code < 400) {
                return "✅ متصل (" + ping + "ms)";
            } else if (code == 401 || code == 405) {
                return "✅ سرور در دسترس (" + ping + "ms)";
            } else {
                return "⚠️ کد وضعیت " + code + " (" + ping + "ms)";
            }

        } catch (Exception e) {
            return "❌ قطع / عدم دسترسی";
        }
    }
}
""",

    "app/src/main/java/ir/nimasirex/aistatus/MainActivity.java": """package ir.nimasirex.aistatus;

import android.content.SharedPreferences;
import android.graphics.Color;
import android.graphics.Typeface;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class MainActivity extends AppCompatActivity {

    private final List<CheckBox> categoryCheckBoxes = new ArrayList<>();
    private final Map<String, TextView> resultViews = new HashMap<>();
    private LinearLayout resultsContainer;
    private EditText apiKeyInput;
    private final ExecutorService executor = Executors.newFixedThreadPool(6);

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        ScrollView scrollView = new ScrollView(this);
        scrollView.setBackgroundColor(Color.parseColor("#0F172A"));

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(36, 36, 36, 48);
        root.setLayoutDirection(View.LAYOUT_DIRECTION_RTL);
        scrollView.addView(root);

        TextView header = new TextView(this);
        header.setText("پینگ‌سنج و وضعیت سرورهای هوش مصنوعی");
        header.setTextColor(Color.parseColor("#38BDF8"));
        header.setTextSize(19);
        header.setTypeface(null, Typeface.BOLD);
        header.setGravity(Gravity.CENTER);
        root.addView(header);

        TextView subHeader = new TextView(this);
        subHeader.setText("۱. خانواده‌های مورد نظر برای بررسی را انتخاب کنید:");
        subHeader.setTextColor(Color.parseColor("#E2E8F0"));
        subHeader.setTextSize(14);
        subHeader.setPadding(0, 28, 0, 12);
        root.addView(subHeader);

        SharedPreferences prefs = getSharedPreferences("AIPrefs", MODE_PRIVATE);

        for (int i = 0; i < ServiceData.CATEGORIES.length; i++) {
            String cat = ServiceData.CATEGORIES[i];
            CheckBox cb = new CheckBox(this);
            cb.setText(cat);
            cb.setTextColor(Color.WHITE);
            cb.setChecked(i == 0);
            categoryCheckBoxes.add(cb);
            root.addView(cb);
        }

        TextView apiTitle = new TextView(this);
        apiTitle.setText("🔑 کلید اختصاصی Gemini API Key (اختیاری - برای تست عمیق):");
        apiTitle.setTextColor(Color.parseColor("#94A3B8"));
        apiTitle.setTextSize(13);
        apiTitle.setPadding(0, 24, 0, 8);
        root.addView(apiTitle);

        apiKeyInput = new EditText(this);
        apiKeyInput.setHint("بدون کلید هم تست درگاه انجام می‌شود...");
        apiKeyInput.setHintTextColor(Color.parseColor("#64748B"));
        apiKeyInput.setTextColor(Color.WHITE);
        apiKeyInput.setText(prefs.getString("gemini_api_key", ""));
        root.addView(apiKeyInput);

        Button testBtn = new Button(this);
        testBtn.setText("🚀 شروع تست سرویس‌های انتخابی");
        testBtn.setBackgroundColor(Color.parseColor("#0284C7"));
        testBtn.setTextColor(Color.WHITE);
        testBtn.setTextSize(15);
        LinearLayout.LayoutParams btnParams = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
        btnParams.setMargins(0, 24, 0, 24);
        root.addView(testBtn, btnParams);

        resultsContainer = new LinearLayout(this);
        resultsContainer.setOrientation(LinearLayout.VERTICAL);
        root.addView(resultsContainer);

        testBtn.setOnClickListener(v -> runSelectedTests());

        setContentView(scrollView);
    }

    private void runSelectedTests() {
        getSharedPreferences("AIPrefs", MODE_PRIVATE)
                .edit()
                .putString("gemini_api_key", apiKeyInput.getText().toString().trim())
                .apply();

        resultsContainer.removeAllViews();
        resultViews.clear();

        List<String> selectedCats = new ArrayList<>();
        for (CheckBox cb : categoryCheckBoxes) {
            if (cb.isChecked()) {
                selectedCats.add(cb.getText().toString());
            }
        }

        if (selectedCats.isEmpty()) {
            Toast.makeText(this, "لطفاً حداقل یک خانواده هوش مصنوعی را تیک بزنید", Toast.LENGTH_SHORT).show();
            return;
        }

        List<ServiceData.AIService> allServices = ServiceData.getAllServices();

        for (String cat : selectedCats) {
            TextView catHeader = new TextView(this);
            catHeader.setText("▪ " + cat);
            catHeader.setTextColor(Color.parseColor("#38BDF8"));
            catHeader.setTypeface(null, Typeface.BOLD);
            catHeader.setTextSize(15);
            catHeader.setPadding(0, 24, 0, 8);
            resultsContainer.addView(catHeader);

            for (ServiceData.AIService s : allServices) {
                if (s.category.equals(cat)) {
                    LinearLayout row = new LinearLayout(this);
                    row.setOrientation(LinearLayout.HORIZONTAL);
                    row.setPadding(16, 14, 16, 14);
                    row.setBackgroundColor(Color.parseColor("#1E293B"));
                    LinearLayout.LayoutParams rp = new LinearLayout.LayoutParams(
                            LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
                    rp.setMargins(0, 6, 0, 6);

                    TextView nameTv = new TextView(this);
                    nameTv.setText(s.name);
                    nameTv.setTextColor(Color.WHITE);
                    nameTv.setTextSize(13);
                    nameTv.setLayoutParams(new LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f));

                    TextView statusTv = new TextView(this);
                    statusTv.setText("⏳ در حال تست...");
                    statusTv.setTextColor(Color.parseColor("#FBBF24"));
                    statusTv.setTextSize(12);

                    row.addView(nameTv);
                    row.addView(statusTv);
                    resultsContainer.addView(row, rp);

                    resultViews.put(s.id, statusTv);

                    executor.execute(() -> {
                        String res = ServiceData.checkService(MainActivity.this, s);
                        runOnUiThread(() -> {
                            TextView tv = resultViews.get(s.id);
                            if (tv != null) {
                                tv.setText(res);
                                if (res.startsWith("✅")) tv.setTextColor(Color.parseColor("#4ADE80"));
                                else if (res.startsWith("⚠️")) tv.setTextColor(Color.parseColor("#FACC15"));
                                else tv.setTextColor(Color.parseColor("#F87171"));
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
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.graphics.Typeface;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class WidgetConfigActivity extends AppCompatActivity {

    private int appWidgetId = AppWidgetManager.INVALID_APPWIDGET_ID;
    private final List<CheckBox> serviceCheckBoxes = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setResult(RESULT_CANCELED);

        Intent intent = getIntent();
        Bundle extras = intent.getExtras();
        if (extras != null) {
            appWidgetId = extras.getInt(AppWidgetManager.EXTRA_APPWIDGET_ID, AppWidgetManager.INVALID_APPWIDGET_ID);
        }
        if (appWidgetId == AppWidgetManager.INVALID_APPWIDGET_ID) {
            finish();
            return;
        }

        ScrollView scrollView = new ScrollView(this);
        scrollView.setBackgroundColor(Color.parseColor("#0F172A"));

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(36, 36, 36, 48);
        root.setLayoutDirection(View.LAYOUT_DIRECTION_RTL);
        scrollView.addView(root);

        TextView title = new TextView(this);
        title.setText("کدام سرویس‌ها روی این ویجت نمایش داده شوند؟");
        title.setTextColor(Color.parseColor("#38BDF8"));
        title.setTextSize(17);
        title.setTypeface(null, Typeface.BOLD);
        title.setPadding(0, 0, 0, 20);
        root.addView(title);

        List<ServiceData.AIService> allServices = ServiceData.getAllServices();
        String currentCat = "";

        for (int i = 0; i < allServices.size(); i++) {
            ServiceData.AIService s = allServices.get(i);
            if (!s.category.equals(currentCat)) {
                currentCat = s.category;
                
