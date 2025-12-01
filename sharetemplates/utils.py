from PIL import Image, ImageDraw
from django.core.files import File
from io import BytesIO
from .models import ShareTemplate, TemplateTag


def create_gradient_template():
    # Image size
    width, height = 1080, 1080
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)

    # Simple vertical gradient (blue to white)
    # Enhanced vertical gradient with finer color transitions
    top_color = (0, 102, 204)    # Blue
    bottom_color = (255, 255, 255)  # White

    for y in range(height):
        # Using a smoother interpolation function (cubic easing)
        ratio = y / (height - 1)

        # Cubic easing function for smoother transition
        eased_ratio = ratio**2 * (3 - 2 * ratio)

        # Floating point calculation for better precision before converting to int
        r = top_color[0] * (1 - eased_ratio) + bottom_color[0] * eased_ratio
        g = top_color[1] * (1 - eased_ratio) + bottom_color[1] * eased_ratio
        b = top_color[2] * (1 - eased_ratio) + bottom_color[2] * eased_ratio

        # Round instead of int for more accurate color representation
        draw.line([(0, y), (width, y)], fill=(round(r), round(g), round(b)))

        # Save to memory
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

    # Create a ShareTemplate instance
    template = ShareTemplate(
        name="Blue Gradient Example",
        template_type="verse",  # or 'prayer', 'quote'
        html_template="""
            <div style='color:white;text-align:center;padding-top:200px;font-size:48px;'>
                {{ text }}<br><small>{{ reference }}</small>
            </div>
        """,
        css_styles="""
            body { margin:0; padding:0; font-family:Arial; background-color:transparent; }
        """,
        is_active=True
    )

    # Optional: Add tags
    tag, _ = TemplateTag.objects.get_or_create(name="Encouragement")
    template.save()
    template.tags.add(tag)

    # Save gradient as preview image
    template.preview_image.save("gradient_example.png", File(buffer))
    template.save()

    print(f"Template '{template.name}' created with gradient preview.")


