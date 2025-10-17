from PIL import Image

# Load your saved plot
img = Image.open("results/regime_plot.png")

# Get original size
w, h = img.size

# Crop: keep top ~60% for a banner shape
banner = img.crop((0, 0, w, int(h * 0.6)))

# Save cropped banner
banner.save("results/regime_banner.png")

print("✅ Saved cropped banner as results/regime_banner.png")
