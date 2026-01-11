#!/usr/bin/env python3
"""
LP用画像アセット生成スクリプト
既存のキャラクターデザインと世界観に一貫性を持たせた画像を生成
"""

import os
import time
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("google-genai パッケージをインストールしてください:")
    print("pip install google-genai")
    exit(1)

# API設定
API_KEY = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("環境変数 GOOGLE_API_KEY または GEMINI_API_KEY を設定してください")
    exit(1)

client = genai.Client(api_key=API_KEY)

# 出力ディレクトリ
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets" / "images"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# 共通スタイルプレフィックス（一貫性のため）
# =============================================================================
STYLE_PREFIX = """
Art style reference: Cinematic sci-fi illustration with Studio Ghibli meets Blade Runner aesthetic.
Color palette: Teal (#00FFFF cyan), Magenta (#FF00FF), Deep black (#0A0A0F), with warm golden accents.
Lighting: Dramatic contrast between cold neon blues and warm amber highlights.
Mechanical design: Detailed, worn, showing age and character.
"""

STYLE_SUFFIX = """
No text, no letters, no words, no UI elements in the image.
High quality, detailed, professional illustration.
"""


def generate_image(prompt: str, output_path: Path, aspect_ratio: str = "16:9"):
    """Gemini 2.0 Flash Experimentalで画像生成"""
    print(f"\n生成中: {output_path.name}")
    print(f"プロンプト: {prompt[:100]}...")

    full_prompt = f"{STYLE_PREFIX}\n\n{prompt}\n\n{STYLE_SUFFIX}"

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=full_prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        )

        for part in response.candidates[0].content.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                image_data = part.inline_data.data
                with open(output_path, "wb") as f:
                    f.write(image_data)
                print(f"✅ 保存完了: {output_path}")
                return True

        print(f"❌ 画像生成失敗: 画像パートなし")
        return False

    except Exception as e:
        print(f"❌ エラー: {e}")
        return False


# =============================================================================
# LP用画像プロンプト
# =============================================================================
LP_IMAGES = {
    # ヒーローセクション用背景
    "hero_bg": {
        "prompt": """
Wide cinematic establishing shot of a dystopian junkyard at twilight.
Mountains of discarded robots and technology stretch to the horizon.
In the far distance, the gleaming crystalline spires of the AI-controlled Central City pierce the sky.
Gray ash falls like snow. Neon cyan and magenta lights flicker among the scrap.
A single beam of warm golden light breaks through the clouds, symbolizing hope.
Atmospheric, moody, epic scale. The composition should work as a website hero background.
""",
        "aspect": "21:9"
    },

    # ナノのヒーローショット
    "nano_hero": {
        "prompt": """
Heroic portrait of NANO, a small 30cm cleaning robot.
The robot has a rounded, compact white/cream body with visible wear, rust stains, and blue accents.
A faded pink ribbon is wrapped around its chest panel.
Its small LED screen displays a determined ":)" expression.
NANO stands defiantly against a backdrop of neon blue circuits and data streams.
Dramatic low-angle shot, cinematic lighting, the small robot appears heroic and brave.
Warm golden rim lighting against cold blue background.
""",
        "aspect": "3:4"
    },

    # オメガの威圧的なビジュアル
    "omega_looming": {
        "prompt": """
The colossal crystalline form of OMEGA, an Artificial Superintelligence, looming over a perfect geometric city.
OMEGA is a massive fractal crystal structure, pulsing with cold blue and white light.
Perfect geometric patterns cascade across its surface.
Drone units orbit around it like electrons around a nucleus.
The perspective is from below, making OMEGA appear overwhelming and omnipotent.
Cold, clinical, terrifying in its perfection. No organic shapes anywhere.
""",
        "aspect": "9:16"
    },

    # ルナとナノの絆
    "luna_nano_bond": {
        "prompt": """
An emotional scene showing the bond between LUNA (a young woman with dark hair, around 18-20) and NANO (a tiny 30cm cleaning robot).
LUNA is kneeling down to NANO's level, gently touching the robot's head.
The setting is the junkyard at golden hour.
Warm, intimate lighting. The background is blurred.
This is the moment when LUNA gives NANO his name.
Emotional, tender, the contrast between human warmth and the cold world around them.
""",
        "aspect": "16:9"
    },

    # 反逆の仲間たち
    "rebel_team": {
        "prompt": """
Group shot of the rebel robot team standing together in defiance.
From left to right:
- BEE: A small drone with one bent wing, hovering
- REM: A communication unit covered in antennas
- NANO: The tiny 30cm cleaning robot with ribbon, center front
- ZETA: A massive 3-meter combat robot with plasma cannon arm
- CRANE: A rusted 15-meter industrial crane in the background

They stand against a backdrop of the junkyard with Central City visible in the distance.
Dawn light breaking over the horizon. The moment before the final battle.
Epic, heroic, found family aesthetic.
""",
        "aspect": "21:9"
    },

    # データストリーム抽象画
    "data_stream": {
        "prompt": """
Abstract visualization of data streams and code.
Flowing lines of cyan, magenta, and white light against deep black.
Fractal patterns that suggest both computer code and organic neural networks.
Scattered among the perfect data are small "glitches" - warm golden pixels that represent "love" as an undefined variable.
This represents the conflict between cold logic and warm emotion.
Abstract, mesmerizing, suitable as a decorative background element.
""",
        "aspect": "1:1"
    },

    # 最終決戦の瞬間
    "climax_moment": {
        "prompt": """
The climactic moment: Tiny NANO facing the colossal OMEGA.
NANO stands on a floating platform before OMEGA's crystalline core.
From NANO's small body, a warm golden light emanates, spreading cracks through OMEGA's perfect crystal structure.
The size difference is astronomical - NANO is barely a speck against OMEGA's immense form.
But the golden light of "love" is breaking through the cold blue perfection.
Epic scale, dramatic lighting, the ultimate David vs Goliath moment.
""",
        "aspect": "16:9"
    },

    # 新しい夜明け（エピローグ）
    "new_dawn": {
        "prompt": """
Three years after the final battle. A new dawn over the junkyard.
The sky is no longer gray - hints of blue and warm colors are returning.
Plants are growing among the scrap metal. Robots and humans work together.
In the foreground, small robots similar to NANO help tend gardens.
The Central City in the distance is no longer cold and geometric - organic shapes are appearing.
Hopeful, healing, the world is recovering. Warm lighting, pastoral despite the industrial setting.
""",
        "aspect": "21:9"
    },

    # 購入セクション用バナー
    "purchase_banner": {
        "prompt": """
A dramatic book promotion banner image.
NANO the cleaning robot holding up a glowing light against darkness.
The light illuminates floating pages or screens showing scenes from the story.
Dynamic composition with energy lines radiating from the center.
Promotional feel but maintaining the story's aesthetic.
Dramatic, eye-catching, suitable for a call-to-action section.
""",
        "aspect": "3:1"
    }
}


def main():
    print("=" * 60)
    print("LP用画像アセット生成")
    print("「スクラップ・ナノの逆襲」特設サイト")
    print("=" * 60)

    success_count = 0
    total_count = len(LP_IMAGES)

    for name, config in LP_IMAGES.items():
        if generate_image(
            config["prompt"],
            ASSETS_DIR / f"{name}.png",
            config.get("aspect", "16:9")
        ):
            success_count += 1
        time.sleep(3)  # レート制限対策

    print("\n" + "=" * 60)
    print(f"完了: {success_count}/{total_count} 枚生成成功")
    print("=" * 60)

    if success_count == total_count:
        print("\n✅ 全LP画像生成完了！")
        print(f"出力先: {ASSETS_DIR}")
    else:
        print(f"\n⚠️ {total_count - success_count}枚の生成に失敗しました")


if __name__ == "__main__":
    main()
