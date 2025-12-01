#!/usr/bin/env python
"""
Stunning template examples with advanced visual features
"""
from sharetemplates.models import ShareTemplate
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'templates_project.settings')
django.setup()


# Stunning verse templates with advanced features
verse_templates = [
    {
        "name": "Divine Aurora",
        "template_type": "verse",
        "gradient_colors": ["#667eea", "#764ba2", "#f093fb", "#f5576c", "#4facfe"],
        "background": "#0f0c29",
        "text_color": "#ffffff",
        "styles": {
            "container": {
                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%)",
                "backgroundSize": "400% 400%",
                "animation": "gradientShift 8s ease infinite",
                "position": "relative",
                "overflow": "hidden"
            },
            "lightRays": {
                "position": "absolute",
                "top": 0,
                "left": 0,
                "right": 0,
                "bottom": 0,
                "background": "radial-gradient(circle at 30% 20%, rgba(255,255,255,0.1) 0%, transparent 50%), radial-gradient(circle at 70% 80%, rgba(255,255,255,0.08) 0%, transparent 50%)",
                "animation": "shimmer 6s ease-in-out infinite alternate"
            },
            "verseText": {
                "fontSize": 22,
                "fontWeight": "300",
                "textAlign": "center",
                "lineHeight": 1.6,
                "textShadow": "0 2px 20px rgba(0,0,0,0.3), 0 0 40px rgba(255,255,255,0.1)",
                "fontFamily": "Georgia, serif",
                "letterSpacing": "0.5px",
                "animation": "textGlow 4s ease-in-out infinite alternate"
            },
            "referenceBadge": {
                "backgroundColor": "rgba(255,255,255,0.15)",
                "backdropFilter": "blur(10px)",
                "borderRadius": 25,
                "padding": "12px 24px",
                "border": "1px solid rgba(255,255,255,0.2)",
                "boxShadow": "0 8px 32px rgba(0,0,0,0.1)",
                "fontSize": 14,
                "fontWeight": "500",
                "letterSpacing": "1px",
                "textTransform": "uppercase"
            },
            "decorativeElements": {
                "position": "absolute",
                "top": "10%",
                "right": "10%",
                "width": 60,
                "height": 60,
                "background": "radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%)",
                "borderRadius": "50%",
                "animation": "float 3s ease-in-out infinite"
            }
        }
    },
    {
        "name": "Golden Scripture",
        "template_type": "verse",
        "gradient_colors": ["#f7971e", "#ffd200", "#ffb347", "#ff8c00"],
        "background": "#1a1a1a",
        "text_color": "#2c1810",
        "styles": {
            "container": {
                "background": "linear-gradient(45deg, #f7971e 0%, #ffd200 30%, #ffb347 60%, #ff8c00 100%)",
                "position": "relative",
                "boxShadow": "inset 0 0 100px rgba(0,0,0,0.1)"
            },
            "goldTexture": {
                "position": "absolute",
                "top": 0,
                "left": 0,
                "right": 0,
                "bottom": 0,
                "background": "repeating-linear-gradient(45deg, transparent, transparent 2px, rgba(255,255,255,0.1) 2px, rgba(255,255,255,0.1) 4px)",
                "opacity": 0.3
            },
            "verseText": {
                "fontSize": 24,
                "fontWeight": "400",
                "textAlign": "center",
                "lineHeight": 1.5,
                "fontFamily": "Playfair Display, serif",
                "textShadow": "2px 2px 4px rgba(0,0,0,0.3), 0 0 10px rgba(255,215,0,0.5)",
                "color": "#2c1810",
                "letterSpacing": "0.3px"
            },
            "referenceBadge": {
                "backgroundColor": "rgba(44,24,16,0.8)",
                "color": "#ffd700",
                "borderRadius": 20,
                "padding": "10px 20px",
                "fontSize": 13,
                "fontWeight": "600",
                "letterSpacing": "1.2px",
                "textTransform": "uppercase",
                "border": "2px solid #ffd700",
                "boxShadow": "0 4px 15px rgba(0,0,0,0.2)"
            },
            "ornaments": {
                "position": "absolute",
                "top": "15px",
                "left": "15px",
                "width": "30px",
                "height": "30px",
                "border": "2px solid rgba(44,24,16,0.3)",
                "borderRadius": "50%",
                "transform": "rotate(45deg)"
            }
        }
    },
    {
        "name": "Celestial Dreams",
        "template_type": "verse",
        "gradient_colors": ["#2196F3", "#21CBF3", "#2196F3", "#9C27B0", "#673AB7"],
        "background": "#0a0a0a",
        "text_color": "#ffffff",
        "styles": {
            "container": {
                "background": "radial-gradient(ellipse at center, #2196F3 0%, #21CBF3 25%, #2196F3 50%, #9C27B0 75%, #673AB7 100%)",
                "position": "relative",
                "overflow": "hidden"
            },
            "stars": {
                "position": "absolute",
                "top": 0,
                "left": 0,
                "right": 0,
                "bottom": 0,
                "background": "radial-gradient(2px 2px at 20px 30px, #fff, transparent), radial-gradient(2px 2px at 40px 70px, #fff, transparent), radial-gradient(1px 1px at 90px 40px, #fff, transparent), radial-gradient(1px 1px at 130px 80px, #fff, transparent), radial-gradient(2px 2px at 160px 30px, #fff, transparent)",
                "backgroundRepeat": "repeat",
                "backgroundSize": "200px 100px",
                "animation": "twinkle 4s linear infinite",
                "opacity": 0.6
            },
            "verseText": {
                "fontSize": 20,
                "fontWeight": "300",
                "textAlign": "center",
                "lineHeight": 1.7,
                "fontFamily": "Lato, sans-serif",
                "textShadow": "0 0 20px rgba(255,255,255,0.5), 0 2px 10px rgba(0,0,0,0.3)",
                "letterSpacing": "0.8px",
                "animation": "etherealGlow 5s ease-in-out infinite alternate"
            },
            "referenceBadge": {
                "backgroundColor": "rgba(255,255,255,0.1)",
                "backdropFilter": "blur(15px)",
                "borderRadius": 30,
                "padding": "15px 30px",
                "border": "1px solid rgba(255,255,255,0.3)",
                "fontSize": 12,
                "fontWeight": "400",
                "letterSpacing": "2px",
                "textTransform": "uppercase",
                "boxShadow": "0 10px 40px rgba(0,0,0,0.2)"
            },
            "nebula": {
                "position": "absolute",
                "top": "20%",
                "left": "10%",
                "width": "200px",
                "height": "200px",
                "background": "radial-gradient(circle, rgba(33,203,243,0.2) 0%, rgba(156,39,176,0.1) 50%, transparent 70%)",
                "borderRadius": "50%",
                "filter": "blur(20px)",
                "animation": "nebulaDrift 10s linear infinite"
            }
        }
    }
]

# Stunning prayer templates
prayer_templates = [
    {
        "name": "Sacred Sunrise",
        "template_type": "prayer",
        "gradient_colors": ["#ff9a9e", "#fecfef", "#fecfef", "#ff9a9e"],
        "background": "#fff5f5",
        "text_color": "#4a4a4a",
        "styles": {
            "container": {
                "background": "linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #ff9a9e 100%)",
                "position": "relative",
                "backgroundSize": "200% 200%",
                "animation": "gentleFlow 12s ease-in-out infinite"
            },
            "sunRays": {
                "position": "absolute",
                "top": "10%",
                "right": "10%",
                "width": "100px",
                "height": "100px",
                "background": "conic-gradient(from 0deg, transparent, rgba(255,255,255,0.3), transparent, rgba(255,255,255,0.3), transparent)",
                "borderRadius": "50%",
                "animation": "rotate 20s linear infinite"
            },
            "prayerText": {
                "fontSize": 18,
                "fontWeight": "400",
                "textAlign": "center",
                "lineHeight": 1.8,
                "fontFamily": "Crimson Text, serif",
                "fontStyle": "italic",
                "textShadow": "0 1px 3px rgba(0,0,0,0.1)",
                "letterSpacing": "0.3px",
                "color": "#4a4a4a"
            },
            "titleText": {
                "fontSize": 28,
                "fontWeight": "300",
                "textAlign": "center",
                "marginBottom": "30px",
                "fontFamily": "Playfair Display, serif",
                "color": "#6b4e71",
                "textShadow": "0 2px 4px rgba(0,0,0,0.1)",
                "letterSpacing": "1px"
            },
            "decorativeBorder": {
                "border": "2px solid rgba(255,255,255,0.4)",
                "borderRadius": "15px",
                "padding": "20px",
                "backdropFilter": "blur(5px)",
                "boxShadow": "0 8px 25px rgba(0,0,0,0.1)"
            }
        }
    },
    {
        "name": "Midnight Reflection",
        "template_type": "prayer",
        "gradient_colors": ["#0f0c29", "#24243e", "#313862", "#4b4376"],
        "background": "#000000",
        "text_color": "#e8e8e8",
        "styles": {
            "container": {
                "background": "linear-gradient(180deg, #0f0c29 0%, #24243e 35%, #313862 70%, #4b4376 100%)",
                "position": "relative",
                "overflow": "hidden"
            },
            "moonlight": {
                "position": "absolute",
                "top": "5%",
                "right": "15%",
                "width": "80px",
                "height": "80px",
                "background": "radial-gradient(circle, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0.4) 40%, transparent 70%)",
                "borderRadius": "50%",
                "boxShadow": "0 0 50px rgba(255,255,255,0.3)",
                "animation": "moonGlow 6s ease-in-out infinite alternate"
            },
            "prayerText": {
                "fontSize": 17,
                "fontWeight": "300",
                "textAlign": "center",
                "lineHeight": 1.9,
                "fontFamily": "Source Serif Pro, serif",
                "color": "#e8e8e8",
                "textShadow": "0 1px 10px rgba(255,255,255,0.1)",
                "letterSpacing": "0.5px"
            },
            "titleText": {
                "fontSize": 26,
                "fontWeight": "200",
                "textAlign": "center",
                "marginBottom": "25px",
                "fontFamily": "Lora, serif",
                "color": "#b8b8d1",
                "textShadow": "0 0 15px rgba(184,184,209,0.5)",
                "letterSpacing": "2px"
            },
            "mysticalAura": {
                "position": "absolute",
                "bottom": "10%",
                "left": "10%",
                "width": "150px",
                "height": "150px",
                "background": "radial-gradient(circle, rgba(75,67,118,0.3) 0%, transparent 70%)",
                "borderRadius": "50%",
                "filter": "blur(30px)",
                "animation": "auraFloat 8s ease-in-out infinite"
            }
        }
    },
    {
        "name": "Forest Sanctuary",
        "template_type": "prayer",
        "gradient_colors": ["#134e5e", "#71b280", "#a8e6cf", "#dcedc1"],
        "background": "#f0f8f0",
        "text_color": "#2d5016",
        "styles": {
            "container": {
                "background": "linear-gradient(45deg, #134e5e 0%, #71b280 35%, #a8e6cf 70%, #dcedc1 100%)",
                "position": "relative",
                "backgroundAttachment": "fixed"
            },
            "leaves": {
                "position": "absolute",
                "top": 0,
                "left": 0,
                "right": 0,
                "bottom": 0,
                "background": "url('data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\"><circle cx=\"20\" cy=\"20\" r=\"2\" fill=\"rgba(255,255,255,0.1)\"/><circle cx=\"80\" cy=\"40\" r=\"1.5\" fill=\"rgba(255,255,255,0.08)\"/><circle cx=\"40\" cy=\"80\" r=\"1\" fill=\"rgba(255,255,255,0.06)\"/></svg>')",
                "backgroundSize": "100px 100px",
                "animation": "leafDrift 15s linear infinite"
            },
            "prayerText": {
                "fontSize": 19,
                "fontWeight": "400",
                "textAlign": "center",
                "lineHeight": 1.7,
                "fontFamily": "Merriweather, serif",
                "color": "#2d5016",
                "textShadow": "0 1px 2px rgba(255,255,255,0.3)",
                "letterSpacing": "0.2px"
            },
            "titleText": {
                "fontSize": 30,
                "fontWeight": "300",
                "textAlign": "center",
                "marginBottom": "35px",
                "fontFamily": "Libre Baskerville, serif",
                "color": "#1a3a0a",
                "textShadow": "0 2px 4px rgba(255,255,255,0.2)",
                "letterSpacing": "1.5px"
            },
            "naturalFrame": {
                "border": "3px solid rgba(45,80,22,0.2)",
                "borderRadius": "25px",
                "padding": "25px",
                "backgroundColor": "rgba(255,255,255,0.1)",
                "backdropFilter": "blur(3px)",
                "boxShadow": "inset 0 0 20px rgba(255,255,255,0.2), 0 10px 30px rgba(0,0,0,0.1)"
            }
        }
    },
    {
        "name": "Royal Elegance",
        "template_type": "prayer",
        "gradient_colors": ["#8360c3", "#2ebf91", "#8360c3", "#2ebf91"],
        "background": "#1a1a2e",
        "text_color": "#f5f5f5",
        "styles": {
            "container": {
                "background": "linear-gradient(135deg, #8360c3 0%, #2ebf91 50%, #8360c3 100%)",
                "position": "relative",
                "backgroundSize": "300% 300%",
                "animation": "royalShimmer 10s ease-in-out infinite"
            },
            "crown": {
                "position": "absolute",
                "top": "8%",
                "left": "50%",
                "transform": "translateX(-50%)",
                "width": "40px",
                "height": "40px",
                "background": "linear-gradient(45deg, #ffd700, #ffed4e)",
                "clipPath": "polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%)",
                "animation": "crownGlow 4s ease-in-out infinite alternate"
            },
            "prayerText": {
                "fontSize": 20,
                "fontWeight": "300",
                "textAlign": "center",
                "lineHeight": 1.8,
                "fontFamily": "Cormorant Garamond, serif",
                "color": "#f5f5f5",
                "textShadow": "0 2px 8px rgba(0,0,0,0.3), 0 0 20px rgba(255,255,255,0.1)",
                "letterSpacing": "0.4px"
            },
            "titleText": {
                "fontSize": 32,
                "fontWeight": "400",
                "textAlign": "center",
                "marginBottom": "40px",
                "fontFamily": "Cinzel, serif",
                "color": "#ffd700",
                "textShadow": "0 3px 6px rgba(0,0,0,0.4), 0 0 25px rgba(255,215,0,0.3)",
                "letterSpacing": "2px",
                "textTransform": "uppercase"
            },
            "royalBorder": {
                "border": "2px solid rgba(255,215,0,0.4)",
                "borderRadius": "20px",
                "padding": "30px",
                "backgroundColor": "rgba(0,0,0,0.1)",
                "backdropFilter": "blur(8px)",
                "boxShadow": "0 15px 35px rgba(0,0,0,0.2), inset 0 0 20px rgba(255,215,0,0.1)"
            }
        }
    }
]


def create_stunning_templates():
    """Create stunning template examples"""

    print("Creating stunning verse templates...")
    for template_data in verse_templates:
        template, created = ShareTemplate.objects.get_or_create(
            name=template_data['name'],
            template_type=template_data['template_type'],
            defaults=template_data
        )
        if created:
            print(f"✨ Created stunning verse template: {template.name}")
        else:
            print(f"Template {template.name} already exists")

    print("\nCreating stunning prayer templates...")
    for template_data in prayer_templates:
        template, created = ShareTemplate.objects.get_or_create(
            name=template_data['name'],
            template_type=template_data['template_type'],
            defaults=template_data
        )
        if created:
            print(f"🙏 Created stunning prayer template: {template.name}")
        else:
            print(f"Template {template.name} already exists")

    print(f"\n🎨 Total templates in database: {ShareTemplate.objects.count()}")
    print("Stunning template creation completed!")

    # Display template features
    print("\n" + "="*60)
    print("STUNNING FEATURES INCLUDED:")
    print("="*60)
    print("🌟 Advanced gradient animations")
    print("✨ Light rays and shimmer effects")
    print("🌙 Celestial elements (stars, moon, nebula)")
    print("🎭 Backdrop blur and glass morphism")
    print("👑 Decorative elements (crowns, ornaments)")
    print("🌿 Nature-inspired animations")
    print("💫 Text glow and shadow effects")
    print("🎨 Premium typography combinations")
    print("🔮 Mystical auras and floating elements")
    print("⭐ Responsive design considerations")


if __name__ == "__main__":
    create_stunning_templates()
