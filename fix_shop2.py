path = r"C:\VEDA_2.0\Frontend\src\App.tsx"
with open(path, encoding='utf-8') as f:
    c = f.read()

# Remove cart emoji from shop header
c = c.replace("🛒 {totalItems} item", "{totalItems} item")
c = c.replace("\U0001f6d2 {totalItems} item", "{totalItems} item")

# Remove search emoji from category buttons
c = c.replace("{ slug: 'all', name: 'All', icon: '🔍' }", "{ slug: 'all', name: 'All', icon: '' }")
c = c.replace("{ slug: 'all', name: 'All', icon: '\U0001f50d' }", "{ slug: 'all', name: 'All', icon: '' }")

# Fix the icon display in category buttons — remove icon prefix entirely
c = c.replace("{'icon' in cat ? cat.icon : ''} {'name' in cat ? cat.name : ''}", "{'name' in cat ? cat.name : ''}")

# Fix shop subtitle text encoding
c = c.replace("{allProducts.length} parts \u00b7 Fast delivery to your workshop",
              "{allProducts.length} parts — Fast delivery to your workshop")

# Fix any remaining Rs symbol garbling (⚹ -> Rs)
c = c.replace("\u2739", "Rs")

# Fix upload arrow emoji in platform page
c = c.replace("⬆  Upload CSV file", "Upload CSV file")
c = c.replace("\u2b06  Upload CSV file", "Upload CSV file")
c = c.replace("⬆ Upload CSV file", "Upload CSV file")

# Fix document emoji in platform page  
c = c.replace("📄 {file.name}", "{file.name}")
c = c.replace("\U0001f4c4 {file.name}", "{file.name}")

# Remove any remaining standalone emojis in text content (not in image src)
import re
# Replace emoji sequences that appear as text content (between > and <)
c = re.sub(r'>\s*[\U0001F300-\U0001F9FF]\s*([^<]*)<', lambda m: '>' + m.group(1) + '<', c)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Done.")
