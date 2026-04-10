"""
Auto Dataset Generator - Core Engine
Generates synthetic datasets for VLM stress-testing at scale (100-10k images)
"""

import os
import json
import random
import sys
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import cv2
from PIL import Image, ImageDraw, ImageFont
import io


class TextBlockLibrary:
    """Manages diverse text blocks for realistic dataset generation"""
    
    def __init__(self):
        """Initialize with 100+ text blocks across categories"""
        self.text_blocks = self._initialize_text_blocks()
    
    def _initialize_text_blocks(self) -> Dict[str, List[str]]:
        """Create 100+ diverse text blocks"""
        
        blocks = {
            'documents': [
                "Contract Agreement\nThis agreement is made between...",
                "Invoice #2024-001\nAmount Due: $1,234.56\nDue Date: 2024-04-15",
                "Purchase Order\nOrder Date: 2024-01-15\nDelivery: 2024-02-15",
                "Receipt\nTransaction ID: TXN-2024-001\nTotal: $99.99",
                "Certificate\nCertified Professional\nValid Until: 2025-12-31",
                "License\nLicense #: AB-123-456\nExpiration: 12/31/2025",
                "Permit\nPermit Type: Building\nIssued: 2024-01-01",
                "Report\nQuarterly Report Q1 2024\nRevenue: $5.2M",
                "Proposal\nProject Proposal 2024\nBudget: $250,000",
                "Schedule\nMeeting Schedule\n9:00 AM - Team Standup",
            ],
            'websites': [
                "Welcome to our website\nBest deals online\nShop now →",
                "Special Offer: 50% Off\nFree Shipping\nLimited Time",
                "Sign In\nEmail: user@example.com\nPassword: ****",
                "Product Title\n★★★★★ (1,234 reviews)\nPrice: $29.99",
                "Add to Cart\nQuantity: 1\nTotal: $29.99",
                "Contact Us\nPhone: (555) 123-4567\nEmail: info@example.com",
                "Privacy Policy\nCookie Settings\nTerms of Service",
                "Newsletter Signup\nEnter your email\nSubscribe →",
                "Featured Products\nNew Arrivals\nBestsellers",
                "Shopping Cart\nItems: 3\nSubtotal: $89.97",
            ],
            'forms': [
                "Application Form\nFull Name: John Doe\nEmail: john@example.com",
                "Feedback Form\nRating: ★★★★☆\nComments: Excellent service!",
                "Registration\nUsername: user123\nPassword: •••••••",
                "Survey\n1. Satisfaction: Very Good\n2. Would recommend: Yes",
                "Tax Form\nIncome: $75,000\nDeductions: $12,000",
                "Medical Form\nDate of Birth: 01/15/1990\nAllergies: None",
                "Employment\nPosition: Engineer\nDepartment: Tech",
                "Shipping Address\n123 Main St\nAnytown, USA 12345",
                "Billing Info\nCard Type: Visa\nExpires: 12/25",
                "Settings Form\nLanguage: English\nTheme: Dark",
            ],
            'multilingual': [
                "Hello World\nBonjour le monde\nHola Mundo",
                "Welcome\n欢迎\nБобро пожаловать",
                "Thank You\nありがとう\nSpasibo",
                "Address: 北京市朝阳区\nBeijing, China",
                "Email: 联系我们\nContact us today",
                "Error: Erreur\nFehler\nエラー",
                "Login\n登录\nAnmelden",
                "Price: ¥299\n€299\n£299",
                "Sale\n销售中\nEn venta",
                "Search... искать... 搜索",
            ],
            'technical': [
                "Code: <div class=\"container\">",
                "API Endpoint\n/api/v1/users\nGET method",
                "Database\nHost: db.example.com\nPort: 5432",
                "Error Log\nERROR: Connection timeout\nTime: 14:32:45",
                "Version: 2.4.1\nRelease Date: 2024-01-15",
                "License: MIT\nAuthor: John Developer",
                "Dependencies\nPython 3.8+\nNode.js 16+",
                "Configuration\nREAD_TIMEOUT=30s\nMAX_RETRIES=3",
                "Metrics\nUptime: 99.99%\nLatency: 45ms",
                "Status: OK\nResponse Time: 234ms",
            ],
            'natural': [
                "The quick brown fox\njumps over the lazy dog",
                "Lorem ipsum dolor sit\namet, consectetur adipiscing",
                "Book Title\nBy Author Name\nPublished 2024",
                "Headlines Today\nWeather: Sunny 72°F\nTop Stories",
                "Recipe: Chocolate Cake\nPrep: 15 min\nBake: 30 min",
                "Menu\nAppetizers\nMain Course\nDesserts",
                "Poster\nEvent: Concert\nDate: June 15",
                "Label: Warning\nHigh Voltage\nDanger",
                "Sign: Exit\n← Emergency Exit →\nDo Not Block",
                "Note: Important\nPlease read carefully\nThank you",
            ]
        }
        
        return blocks
    
    def get_random_block(self, category: Optional[str] = None) -> str:
        """Get a random text block"""
        if category and category in self.text_blocks:
            blocks = self.text_blocks[category]
        else:
            all_blocks = []
            for cat_blocks in self.text_blocks.values():
                all_blocks.extend(cat_blocks)
            blocks = all_blocks
        
        return random.choice(blocks)
    
    def get_blocks_by_category(self, category: str) -> List[str]:
        """Get all blocks in a category"""
        return self.text_blocks.get(category, [])
    
    def get_all_categories(self) -> List[str]:
        """Get all available categories"""
        return list(self.text_blocks.keys())


class BackgroundLibrary:
    """Manages diverse background images for realistic rendering"""
    
    def __init__(self):
        """Initialize synthetic background generation"""
        self.backgrounds = None
    
    def generate_synthetic_backgrounds(self, count: int = 20) -> List[np.ndarray]:
        """Generate synthetic backgrounds across realistic families"""
        
        backgrounds = []

        family_generators = [
            self._create_paper_texture,
            self._create_notebook_textbook_page,
            self._create_newspaper_page,
            self._create_ad_flyer_layout,
            self._create_office_document,
            self._create_screen_ui_capture,
            self._create_signage_outdoor,
            self._create_packaging_label,
            self._create_low_light_photo_capture,
            self._create_solid_color,
            self._create_gradient,
            self._create_noisy_bg,
            self._create_pattern,
        ]

        for i in range(count):
            generator = family_generators[i % len(family_generators)]
            bg = generator()
            backgrounds.append(bg)
        
        return backgrounds
    
    def _create_paper_texture(self, width: int = 800, height: int = 600) -> np.ndarray:
        """Create paper-like textures: plain, ruled, aged, crumpled, photocopy shadow"""
        style = random.choice(["plain", "ruled", "aged", "crumpled", "photocopy"])
        base = 238 if style != "aged" else random.randint(210, 228)
        bg = np.ones((height, width, 3), dtype=np.uint8) * base

        noise = np.random.normal(0, 4, (height, width, 3))
        bg = np.clip(bg + noise, 0, 255).astype(np.uint8)

        if style == "ruled":
            for y in range(40, height, 28):
                cv2.line(bg, (0, y), (width, y), (220, 225, 235), 1)
            cv2.line(bg, (80, 0), (80, height), (220, 200, 200), 1)

        elif style == "aged":
            tint = np.full_like(bg, (200, 220, 235), dtype=np.uint8)
            bg = cv2.addWeighted(bg, 0.78, tint, 0.22, 0)
            cv2.rectangle(bg, (0, 0), (width - 1, height - 1), (180, 190, 200), 2)

        elif style == "crumpled":
            for _ in range(20):
                x1, y1 = random.randint(0, width - 1), random.randint(0, height - 1)
                x2 = min(width - 1, max(0, x1 + random.randint(-140, 140)))
                y2 = min(height - 1, max(0, y1 + random.randint(-90, 90)))
                shade = random.randint(205, 235)
                cv2.line(bg, (x1, y1), (x2, y2), (shade, shade, shade), 1)

        elif style == "photocopy":
            left_shadow = np.linspace(22, 0, max(1, width // 5), dtype=np.uint8)
            bg[:, :left_shadow.size, :] = np.clip(
                bg[:, :left_shadow.size, :] - left_shadow[np.newaxis, :, np.newaxis], 0, 255
            )
            for _ in range(6):
                y = random.randint(20, height - 20)
                cv2.line(bg, (0, y), (width, y), (225, 225, 225), 1)

        return bg
    
    def _create_gradient(self, width: int = 800, height: int = 600) -> np.ndarray:
        """Create gradient background"""
        bg = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Random color gradient
        colors = [
            ((200, 220, 255), (255, 200, 200)),  # Blue to red
            ((255, 240, 200), (200, 220, 255)),  # Orange to blue
            ((200, 255, 220), (220, 200, 255)),  # Green to purple
        ]
        
        color1, color2 = random.choice(colors)
        
        for y in range(height):
            ratio = y / height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            bg[y, :] = (b, g, r)
        
        return bg
    
    def _create_noisy_bg(self, width: int = 800, height: int = 600) -> np.ndarray:
        """Create noisy background"""
        base = random.randint(200, 240)
        bg = np.ones((height, width, 3), dtype=np.uint8) * base
        
        noise = np.random.normal(0, 10, (height, width, 3))
        bg = np.clip(bg + noise, 0, 255).astype(np.uint8)
        
        return bg
    
    def _create_pattern(self, width: int = 800, height: int = 600) -> np.ndarray:
        """Create patterned background"""
        bg = np.ones((height, width, 3), dtype=np.uint8) * 220
        
        # Create checkerboard or stripe pattern
        pattern_type = random.choice(['checkerboard', 'stripes', 'dots'])
        
        if pattern_type == 'checkerboard':
            square_size = 40
            for y in range(0, height, square_size):
                for x in range(0, width, square_size):
                    if ((x // square_size) + (y // square_size)) % 2:
                        bg[y:y+square_size, x:x+square_size] = 210
        
        elif pattern_type == 'stripes':
            for y in range(0, height, 20):
                bg[y:y+10, :] = 200
        
        else:  # dots
            for _ in range(50):
                x = random.randint(0, width)
                y = random.randint(0, height)
                cv2.circle(bg, (x, y), 5, (200, 200, 200), -1)
        
        return bg
    
    def _create_solid_color(self, width: int = 800, height: int = 600) -> np.ndarray:
        """Create solid color with subtle texture and vignette"""
        color_options = [
            (240, 240, 240),  # Light gray
            (245, 245, 250),  # Light blue
            (250, 245, 240),  # Light orange
            (245, 250, 245),  # Light green
            (232, 238, 246),
            (244, 236, 230),
        ]
        
        color = random.choice(color_options)
        bg = np.ones((height, width, 3), dtype=np.uint8)
        bg[:, :] = color

        noise = np.random.normal(0, 2.0, (height, width, 3))
        bg = np.clip(bg + noise, 0, 255).astype(np.uint8)

        yy, xx = np.mgrid[0:height, 0:width]
        cx, cy = width / 2.0, height / 2.0
        radius = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        vignette = 1.0 - 0.12 * (radius / (max(width, height) / 1.2))
        vignette = np.clip(vignette, 0.86, 1.0)
        bg = np.clip(bg * vignette[:, :, None], 0, 255).astype(np.uint8)
        
        return bg

    def _create_notebook_textbook_page(self, width: int = 800, height: int = 600) -> np.ndarray:
        """Notebook/textbook pages: lines, columns, notes, highlights"""
        bg = self._create_paper_texture(width, height)
        mode = random.choice(["notebook", "textbook"])

        if mode == "notebook":
            for y in range(36, height, 30):
                cv2.line(bg, (0, y), (width, y), (218, 223, 236), 1)
            cv2.line(bg, (90, 0), (90, height), (210, 180, 185), 2)
            for _ in range(6):
                x1 = random.randint(120, width - 200)
                y = random.randint(30, height - 30)
                x2 = min(width - 10, x1 + random.randint(120, 220))
                cv2.line(bg, (x1, y), (x2, y), (245, 245, 190), random.randint(8, 16))
        else:
            gutter = width // 2
            cv2.line(bg, (gutter, 20), (gutter, height - 20), (212, 212, 212), 2)
            for _ in range(18):
                y = random.randint(24, height - 24)
                x1 = random.randint(30, gutter - 120)
                x2 = random.randint(gutter + 30, width - 120)
                cv2.line(bg, (x1, y), (x1 + random.randint(80, 160), y), (185, 185, 185), 1)
                cv2.line(bg, (x2, y), (x2 + random.randint(80, 160), y), (185, 185, 185), 1)

        return bg

    def _create_newspaper_page(self, width: int = 800, height: int = 600) -> np.ndarray:
        """Newspaper style: columns, grayscale print, fold/scan artifacts"""
        bg = np.ones((height, width, 3), dtype=np.uint8) * random.randint(205, 224)
        num_cols = random.choice([3, 4, 5])
        col_w = width // num_cols

        for c in range(num_cols):
            x0 = c * col_w + 8
            for y in range(20, height - 20, random.randint(12, 18)):
                line_len = random.randint(col_w // 2, col_w - 20)
                shade = random.randint(110, 165)
                cv2.line(bg, (x0, y), (x0 + line_len, y), (shade, shade, shade), 1)

        for c in range(1, num_cols):
            x = c * col_w
            cv2.line(bg, (x, 0), (x, height), (188, 188, 188), 1)

        # Fold line + scan noise/ink bleed
        fold_x = random.randint(width // 4, 3 * width // 4)
        cv2.line(bg, (fold_x, 0), (fold_x, height), (175, 175, 175), 2)
        blur = cv2.GaussianBlur(bg, (3, 3), 0)
        bg = cv2.addWeighted(bg, 0.9, blur, 0.1, 0)
        scan_noise = np.random.normal(0, 6, (height, width, 1))
        bg = np.clip(bg + scan_noise, 0, 255).astype(np.uint8)
        return bg

    def _create_ad_flyer_layout(self, width: int = 800, height: int = 600) -> np.ndarray:
        """Promotional layouts: posters, coupons, brochure panels, tags"""
        bg = self._create_gradient(width, height)
        for _ in range(random.randint(4, 9)):
            x1 = random.randint(10, width - 180)
            y1 = random.randint(10, height - 120)
            w = random.randint(120, 260)
            h = random.randint(60, 170)
            x2, y2 = min(width - 5, x1 + w), min(height - 5, y1 + h)
            color = tuple(int(v) for v in np.random.randint(150, 255, size=3))
            cv2.rectangle(bg, (x1, y1), (x2, y2), color, -1)
            cv2.rectangle(bg, (x1, y1), (x2, y2), (230, 230, 230), 2)
            if random.random() < 0.45:
                cv2.circle(bg, (x1 + 20, y1 + 20), 10, (245, 245, 245), -1)
        return bg

    def _create_office_document(self, width: int = 800, height: int = 600) -> np.ndarray:
        """Office docs: invoices/forms/receipts/letterheads/stamps"""
        bg = self._create_paper_texture(width, height)
        cv2.rectangle(bg, (20, 20), (width - 20, height - 20), (205, 205, 205), 2)
        cv2.rectangle(bg, (20, 20), (width - 20, 95), (235, 238, 245), -1)
        for y in range(120, height - 40, 34):
            cv2.line(bg, (40, y), (width - 40, y), (190, 190, 190), 1)
        for x in [width // 3, (2 * width) // 3]:
            cv2.line(bg, (x, 120), (x, height - 40), (200, 200, 200), 1)
        # stamp
        stamp_c = (random.randint(90, 150), random.randint(90, 150), random.randint(170, 220))
        cv2.circle(bg, (width - 120, 130), 46, stamp_c, 2)
        return bg

    def _create_screen_ui_capture(self, width: int = 800, height: int = 600) -> np.ndarray:
        """UI-like backgrounds: web pages, chat bubbles, dashboards"""
        bg = np.ones((height, width, 3), dtype=np.uint8) * random.randint(236, 246)
        cv2.rectangle(bg, (0, 0), (width, 64), (225, 230, 240), -1)
        for _ in range(random.randint(8, 16)):
            x1 = random.randint(16, width - 180)
            y1 = random.randint(80, height - 70)
            w = random.randint(90, 260)
            h = random.randint(20, 68)
            x2, y2 = min(width - 12, x1 + w), min(height - 12, y1 + h)
            card = (random.randint(245, 255), random.randint(245, 255), random.randint(245, 255))
            cv2.rectangle(bg, (x1, y1), (x2, y2), card, -1)
            cv2.rectangle(bg, (x1, y1), (x2, y2), (220, 225, 232), 1)
        return bg

    def _create_signage_outdoor(self, width: int = 800, height: int = 600) -> np.ndarray:
        """Outdoor signage: boards, banners, notices on textured walls"""
        bg = np.ones((height, width, 3), dtype=np.uint8) * random.randint(150, 210)
        wall_noise = np.random.normal(0, 14, (height, width, 3))
        bg = np.clip(bg + wall_noise, 0, 255).astype(np.uint8)
        for _ in range(random.randint(2, 5)):
            x1 = random.randint(30, width - 280)
            y1 = random.randint(30, height - 180)
            w = random.randint(180, 300)
            h = random.randint(90, 170)
            x2, y2 = min(width - 10, x1 + w), min(height - 10, y1 + h)
            color = tuple(int(v) for v in np.random.randint(60, 220, size=3))
            cv2.rectangle(bg, (x1, y1), (x2, y2), color, -1)
            cv2.rectangle(bg, (x1, y1), (x2, y2), (35, 35, 35), 2)
        return bg

    def _create_packaging_label(self, width: int = 800, height: int = 600) -> np.ndarray:
        """Packaging/labels: stickers, medicine labels, barcode zones"""
        bg = np.ones((height, width, 3), dtype=np.uint8) * random.randint(210, 240)
        for _ in range(random.randint(3, 7)):
            x1 = random.randint(20, width - 260)
            y1 = random.randint(20, height - 140)
            w = random.randint(150, 260)
            h = random.randint(70, 140)
            x2, y2 = min(width - 8, x1 + w), min(height - 8, y1 + h)
            cv2.rectangle(bg, (x1, y1), (x2, y2), (248, 248, 248), -1)
            cv2.rectangle(bg, (x1, y1), (x2, y2), (180, 180, 180), 2)
            # simple barcode region
            if random.random() < 0.8:
                bx1, by1 = x1 + 10, y2 - 28
                for b in range(22):
                    bx = bx1 + b * 4
                    if random.random() < 0.65:
                        cv2.line(bg, (bx, by1), (bx, y2 - 8), (25, 25, 25), 1)
        return bg

    def _create_low_light_photo_capture(self, width: int = 800, height: int = 600) -> np.ndarray:
        """Photo-captured feel: uneven lighting, shadows, perspective, mild blur"""
        bg = self._create_office_document(width, height)
        bg = bg.astype(np.float32)

        # uneven light gradient
        gx = np.linspace(0.65, 1.12, width, dtype=np.float32)
        gy = np.linspace(0.85, 1.05, height, dtype=np.float32)
        light = gy[:, None] * gx[None, :]
        bg *= light[:, :, None]

        # soft shadow blob
        cx, cy = random.randint(0, width), random.randint(0, height)
        yy, xx = np.mgrid[0:height, 0:width]
        dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        shadow = np.clip(1.0 - 0.25 * np.exp(-(dist ** 2) / (2 * (0.22 * width) ** 2)), 0.72, 1.0)
        bg *= shadow[:, :, None]
        bg = np.clip(bg, 0, 255).astype(np.uint8)

        # mild blur + perspective tilt
        bg = cv2.GaussianBlur(bg, (3, 3), 0.8)
        src = np.float32([[0, 0], [width - 1, 0], [0, height - 1], [width - 1, height - 1]])
        dx = random.uniform(6, 24)
        dy = random.uniform(4, 20)
        dst = np.float32([[dx, dy], [width - 1 - dx, 0], [0, height - 1], [width - 1, height - 1 - dy]])
        mat = cv2.getPerspectiveTransform(src, dst)
        bg = cv2.warpPerspective(bg, mat, (width, height), borderMode=cv2.BORDER_REFLECT)
        return bg
    
    def get_backgrounds(self, count: int = 20) -> List[np.ndarray]:
        """Get or generate backgrounds"""
        if self.backgrounds is None:
            self.backgrounds = self.generate_synthetic_backgrounds(count)
        return self.backgrounds


class ImageRenderer:
    """Renders text on images with various fonts and styles"""
    
    def __init__(self):
        """Initialize renderer"""
        self.fonts = self._get_available_fonts()
    
    def _get_available_fonts(self) -> Dict[str, str]:
        """Get available system fonts"""
        fonts = {
            'regular': None,  # Will use PIL default
            'bold': None,
            'mono': None,
            'fallback': None,
        }
        
        # Try to find actual fonts on system
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
            "/System/Library/Fonts/Helvetica.ttc",  # macOS
            "C:\\Windows\\Fonts\\arial.ttf",  # Windows
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",  # Linux alt
        ]
        
        for path in font_paths:
            if os.path.exists(path):
                fonts['regular'] = path
                break

        fallback_paths = [
            "C:\\Windows\\Fonts\\Nirmala.ttf",
            "C:\\Windows\\Fonts\\segoeui.ttf",
            "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        ]
        for path in fallback_paths:
            if os.path.exists(path):
                fonts['fallback'] = path
                break
        
        return fonts

    def _load_font(self, size: int, use_fallback: bool = False):
        """Load a font file if available, otherwise use PIL default."""
        try:
            if use_fallback and self.fonts.get('fallback'):
                return ImageFont.truetype(self.fonts['fallback'], size)
            if self.fonts.get('regular'):
                return ImageFont.truetype(self.fonts['regular'], size)
            return ImageFont.load_default()
        except Exception:
            return ImageFont.load_default()

    def _draw_text_with_kerning_jitter(
        self,
        draw: ImageDraw.ImageDraw,
        text: str,
        x: int,
        y: int,
        font,
        color: Tuple[int, int, int],
        jitter_strength: float
    ) -> None:
        """Render text with uneven glyph spacing to simulate kerning artifacts."""
        cursor_x = float(x)
        for ch in text:
            draw.text((cursor_x, y), ch, fill=color, font=font)
            char_w = draw.textlength(ch, font=font)
            spacing_jitter = random.uniform(-jitter_strength, jitter_strength)
            cursor_x += max(1.0, char_w + spacing_jitter)
    
    def render_text_on_image(
        self,
        image: np.ndarray,
        text: str,
        font_size: int = 24,
        color: Tuple[int, int, int] = (0, 0, 0),
        position: str = "center",
        background: bool = False
    ) -> np.ndarray:
        """Render text on image"""
        
        # Convert OpenCV image to PIL
        if len(image.shape) == 3:
            pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        else:
            pil_image = Image.fromarray(image)
        
        draw = ImageDraw.Draw(pil_image)
        
        # Load font
        try:
            if self.fonts['regular']:
                font = ImageFont.truetype(self.fonts['regular'], font_size)
            else:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Calculate position
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        if position == "center":
            x = (pil_image.width - text_width) // 2
            y = (pil_image.height - text_height) // 2
        elif position == "top":
            x = (pil_image.width - text_width) // 2
            y = 20
        else:  # bottom
            x = (pil_image.width - text_width) // 2
            y = pil_image.height - text_height - 20
        
        # Draw background if needed
        if background:
            padding = 10
            draw.rectangle(
                [x - padding, y - padding, x + text_width + padding, y + text_height + padding],
                fill=(255, 255, 255),
                outline=(200, 200, 200)
            )
        
        # Draw text
        draw.text((x, y), text, fill=color, font=font)
        
        # Convert back to OpenCV
        image_with_text = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        return image_with_text
    
    def multi_line_text(
        self,
        image: np.ndarray,
        text: str,
        font_size: int = 20,
        line_spacing: int = 10,
        return_bbox: bool = False
    ):
        """Render multi-line text and optionally return a text bounding box."""
        
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_image)
        
        try:
            if self.fonts['regular']:
                font = ImageFont.truetype(self.fonts['regular'], font_size)
            else:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        lines = text.split('\n')
        
        # Calculate total height
        total_height = 0
        line_heights = []
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            line_height = bbox[3] - bbox[1]
            line_heights.append(line_height)
            total_height += line_height + line_spacing
        
        # Calculate starting Y
        start_y = (pil_image.height - total_height) // 2
        
        # Draw lines
        y = start_y
        min_x, min_y = pil_image.width, pil_image.height
        max_x, max_y = 0, 0
        for line, line_height in zip(lines, line_heights):
            bbox = draw.textbbox((0, 0), line, font=font)
            line_width = bbox[2] - bbox[0]
            x = (pil_image.width - line_width) // 2
            draw.text((x, y), line, fill=(0, 0, 0), font=font)
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x + line_width)
            max_y = max(max_y, y + line_height)
            y += line_height + line_spacing
        
        # Convert back
        image_with_text = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        if not lines:
            text_bbox = (0, 0, 0, 0)
        else:
            text_bbox = (int(min_x), int(min_y), int(max_x), int(max_y))

        if return_bbox:
            return image_with_text, text_bbox
        return image_with_text

    def multi_line_text_with_typography_artifacts(
        self,
        image: np.ndarray,
        text: str,
        artifact_strength: float = 0.6,
        layout_artifact_strength: float = 0.0,
        visual_artifact_strength: float = 0.0,
        styling_artifact_strength: float = 0.0,
        return_bbox: bool = False
    ):
        """
        Render text with typography defects:
        - font mismatch
        - non-uniform line sizing around heading/body/attribution hierarchy
        - uneven kerning/letter spacing
        - center alignment drift
        - semantic line-break degradation
        - contrast mismatch from white text pills/boxes
        - inconsistent line spacing unrelated to font size
        - missing attribution styling (last line not visually separated)
        """
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_image)

        lines = text.split('\n')
        if not lines:
            if return_bbox:
                return image, (0, 0, 0, 0)
            return image

        # Degrade line-break semantics by re-chunking text into arbitrary line groups.
        if layout_artifact_strength > 0 and random.random() < layout_artifact_strength:
            tokenized = " ".join([ln.strip() for ln in lines if ln.strip()]).split()
            if len(tokenized) >= 6:
                new_lines = []
                cursor = 0
                while cursor < len(tokenized):
                    # Smaller chunks increase semantic disruption of phrase grouping.
                    chunk = random.randint(2, 5)
                    new_lines.append(" ".join(tokenized[cursor:cursor + chunk]))
                    cursor += chunk
                if len(new_lines) > 1:
                    lines = new_lines

        # Intended hierarchy: heading (large), body (medium), attribution (small)
        base_sizes = []
        for idx in range(len(lines)):
            if idx == 0:
                base_sizes.append(34)
            elif idx == len(lines) - 1:
                base_sizes.append(18)
            else:
                base_sizes.append(24)

        actual_sizes = []
        for base in base_sizes:
            if random.random() < artifact_strength:
                size = int(base * random.uniform(0.7, 1.25))
            else:
                size = base
            actual_sizes.append(max(12, size))

        missing_attribution_styling = (
            len(lines) >= 2 and styling_artifact_strength > 0 and random.random() < styling_artifact_strength
        )
        if missing_attribution_styling:
            # Make attribution line look like normal body text (no hierarchy).
            body_idx = 1 if len(actual_sizes) > 2 else 0
            actual_sizes[-1] = actual_sizes[body_idx]

        line_fonts = []
        for idx, _ in enumerate(lines):
            use_mismatch = random.random() < artifact_strength
            line_fonts.append(self._load_font(actual_sizes[idx], use_fallback=use_mismatch))

        line_heights = []
        for line, font in zip(lines, line_fonts):
            bbox = draw.textbbox((0, 0), line, font=font)
            line_heights.append(bbox[3] - bbox[1])

        if visual_artifact_strength > 0:
            # Intentionally non-proportional line spacing to simulate rendering/layout bugs.
            line_spacings = []
            for _ in range(max(0, len(lines) - 1)):
                base = random.randint(4, 20)
                jitter = random.uniform(-8.0, 8.0) * visual_artifact_strength
                line_spacings.append(max(0, int(base + jitter)))
        else:
            line_spacings = [10] * max(0, len(lines) - 1)

        if missing_attribution_styling and line_spacings:
            # Collapse spacing before attribution to weaken visual separation.
            line_spacings[-1] = random.randint(0, 3)

        total_height = sum(line_heights) + sum(line_spacings)

        # Sub-pixel-style center misalignment (very subtle for mild artifacts).
        x_offset = random.uniform(-2.0, 2.0) * layout_artifact_strength
        y_offset = random.uniform(-1.5, 1.5) * layout_artifact_strength

        y = (pil_image.height - total_height) // 2 + y_offset

        kerning_jitter = 2.5 * artifact_strength
        min_x, min_y = pil_image.width, pil_image.height
        max_x, max_y = 0, 0
        for idx, (line, font, line_h) in enumerate(zip(lines, line_fonts, line_heights)):
            line_w = int(draw.textlength(line, font=font))
            x = (pil_image.width - line_w) // 2 + x_offset

            # Contrast mismatch artifact: add unnecessary white boxes behind text.
            pill_pad_x = 0
            pill_pad_y = 0
            if visual_artifact_strength > 0 and random.random() < visual_artifact_strength:
                pill_pad_x = int(6 + 10 * visual_artifact_strength)
                pill_pad_y = int(3 + 6 * visual_artifact_strength)
                draw.rectangle(
                    [
                        int(x) - pill_pad_x,
                        int(y) - pill_pad_y,
                        int(x) + line_w + pill_pad_x,
                        int(y) + line_h + pill_pad_y
                    ],
                    fill=(255, 255, 255),
                    outline=(235, 235, 235)
                )

            self._draw_text_with_kerning_jitter(
                draw=draw,
                text=line,
                x=int(x),
                y=int(y),
                font=font,
                color=(0, 0, 0),
                jitter_strength=kerning_jitter
            )
            min_x = min(min_x, int(x) - pill_pad_x)
            min_y = min(min_y, int(y) - pill_pad_y)
            max_x = max(max_x, int(x) + line_w + pill_pad_x)
            max_y = max(max_y, int(y) + line_h + pill_pad_y)
            spacing = line_spacings[idx] if idx < len(line_spacings) else 0
            y += line_h + spacing

        rendered = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        text_bbox = (int(min_x), int(min_y), int(max_x), int(max_y))
        if return_bbox:
            return rendered, text_bbox
        return rendered


class DatasetGenerator:
    """
    Main dataset generator for VLM stress-test datasets.

    Design guarantees:
    - One shared source background per sample group (`input/expected/A/B/C`)
    - Artifact operations are applied in text bounding-box regions
    - Metadata includes per-variant issue labels and text bounding boxes
    """
    
    def __init__(
        self,
        output_dir: str = "./dataset",
        image_size: Tuple[int, int] = (800, 600),
        num_samples: int = 100,
        enable_typography_artifacts: bool = True,
        typography_artifact_strength_a: float = 0.35,
        typography_artifact_strength_c: float = 0.85,
        enable_layout_artifacts: bool = True,
        layout_artifact_strength_a: float = 0.25,
        layout_artifact_strength_c: float = 0.7,
        enable_visual_artifacts: bool = True,
        visual_artifact_strength_a: float = 0.3,
        visual_artifact_strength_c: float = 0.8,
        enable_styling_artifacts: bool = True,
        styling_artifact_strength_a: float = 0.25,
        styling_artifact_strength_c: float = 0.7
    ):
        """Initialize dataset generator"""
        self.output_dir = Path(output_dir)
        self.image_size = image_size
        self.num_samples = num_samples
        self.enable_typography_artifacts = enable_typography_artifacts
        self.typography_artifact_strength_a = max(0.0, min(1.0, typography_artifact_strength_a))
        self.typography_artifact_strength_c = max(0.0, min(1.0, typography_artifact_strength_c))
        self.enable_layout_artifacts = enable_layout_artifacts
        self.layout_artifact_strength_a = max(0.0, min(1.0, layout_artifact_strength_a))
        self.layout_artifact_strength_c = max(0.0, min(1.0, layout_artifact_strength_c))
        self.enable_visual_artifacts = enable_visual_artifacts
        self.visual_artifact_strength_a = max(0.0, min(1.0, visual_artifact_strength_a))
        self.visual_artifact_strength_c = max(0.0, min(1.0, visual_artifact_strength_c))
        self.enable_styling_artifacts = enable_styling_artifacts
        self.styling_artifact_strength_a = max(0.0, min(1.0, styling_artifact_strength_a))
        self.styling_artifact_strength_c = max(0.0, min(1.0, styling_artifact_strength_c))
        
        self.text_library = TextBlockLibrary()
        self.background_library = BackgroundLibrary()
        self.renderer = ImageRenderer()
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate dataset info
        self.dataset_name = f"VLM_Dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.dataset_dir = self.output_dir / self.dataset_name
        self.dataset_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(self) -> str:
        """Generate a full dataset folder and return its path."""
        
        print(f"Generating {self.num_samples} samples...")
        
        backgrounds = self.background_library.get_backgrounds(20)
        samples = []
        
        for idx in range(self.num_samples):
            sample_name = f"img_{idx + 1:04d}"
            sample_dir = self.dataset_dir / sample_name
            sample_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate sample
            sample_info = self._generate_sample(
                sample_dir,
                sample_name,
                backgrounds,
                idx
            )
            samples.append(sample_info)
            
            if (idx + 1) % 10 == 0:
                print(f"  Generated {idx + 1}/{self.num_samples} samples")
        
        # Create manifest
        self._create_manifest(samples)
        
        print(f"Dataset created at: {self.dataset_dir}")
        return str(self.dataset_dir)

    def _normalize_bbox(self, bbox: Tuple[int, int, int, int], width: int, height: int) -> Tuple[int, int, int, int]:
        """Clamp bbox to image bounds and guarantee non-negative area."""
        x1, y1, x2, y2 = bbox
        x1 = max(0, min(width - 1, int(x1)))
        y1 = max(0, min(height - 1, int(y1)))
        x2 = max(x1 + 1, min(width, int(x2)))
        y2 = max(y1 + 1, min(height, int(y2)))
        return x1, y1, x2, y2

    def _apply_gaussian_blur_in_bbox(
        self,
        image: np.ndarray,
        bbox: Tuple[int, int, int, int],
        kernel: Tuple[int, int],
        sigma: float
    ) -> np.ndarray:
        x1, y1, x2, y2 = self._normalize_bbox(bbox, image.shape[1], image.shape[0])
        out = image.copy()
        roi = out[y1:y2, x1:x2]
        out[y1:y2, x1:x2] = cv2.GaussianBlur(roi, kernel, sigma)
        return out

    def _apply_jpeg_artifacts_in_bbox(
        self,
        image: np.ndarray,
        bbox: Tuple[int, int, int, int],
        quality: int
    ) -> np.ndarray:
        x1, y1, x2, y2 = self._normalize_bbox(bbox, image.shape[1], image.shape[0])
        out = image.copy()
        roi = out[y1:y2, x1:x2]
        ok, compressed = cv2.imencode('.jpg', roi, [cv2.IMWRITE_JPEG_QUALITY, quality])
        if ok:
            out[y1:y2, x1:x2] = cv2.imdecode(compressed, cv2.IMREAD_COLOR)
        return out

    def _apply_noise_in_bbox(
        self,
        image: np.ndarray,
        bbox: Tuple[int, int, int, int],
        sigma: float = 15.0
    ) -> np.ndarray:
        x1, y1, x2, y2 = self._normalize_bbox(bbox, image.shape[1], image.shape[0])
        out = image.copy()
        roi = out[y1:y2, x1:x2].astype(np.float32)
        noise = np.random.normal(0, sigma, roi.shape).astype(np.float32)
        roi_noisy = np.clip(roi + noise, 0, 255).astype(np.uint8)
        out[y1:y2, x1:x2] = roi_noisy
        return out

    def _apply_color_shift_in_bbox(
        self,
        image: np.ndarray,
        bbox: Tuple[int, int, int, int],
        alpha: float,
        beta: float
    ) -> np.ndarray:
        x1, y1, x2, y2 = self._normalize_bbox(bbox, image.shape[1], image.shape[0])
        out = image.copy()
        out[y1:y2, x1:x2] = cv2.convertScaleAbs(out[y1:y2, x1:x2], alpha=alpha, beta=beta)
        return out

    def _apply_luma_equalize_in_bbox(
        self,
        image: np.ndarray,
        bbox: Tuple[int, int, int, int]
    ) -> np.ndarray:
        x1, y1, x2, y2 = self._normalize_bbox(bbox, image.shape[1], image.shape[0])
        out = image.copy()
        roi = out[y1:y2, x1:x2]
        lab = cv2.cvtColor(roi, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        l = cv2.equalizeHist(l)
        enhanced = cv2.merge([l, a, b])
        out[y1:y2, x1:x2] = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        return out
    
    def _generate_sample(
        self,
        sample_dir: Path,
        sample_name: str,
        backgrounds: List[np.ndarray],
        index: int
    ) -> Dict:
        """
        Generate one sample group (`input/expected/A/B/C`) plus `meta.json`.

        All five images share the same source background, while A/B/C apply
        variant behavior in text-region bounding boxes.
        """
        
        # Select random background
        background = random.choice(backgrounds).copy()
        
        # Get text block
        text = self.text_library.get_random_block()
        original_text = text
        
        # Generate input (clear text on background)
        input_img, input_bbox = self.renderer.multi_line_text(
            background.copy(),
            text,
            font_size=22,
            return_bbox=True
        )
        cv2.imwrite(str(sample_dir / "input.jpg"), input_img, [cv2.IMWRITE_JPEG_QUALITY, 100])
        
        # Generate expected (perfect - same as input)
        expected_img = input_img.copy()
        expected_bbox = input_bbox
        cv2.imwrite(str(sample_dir / "expected.jpg"), expected_img, [cv2.IMWRITE_JPEG_QUALITY, 100])
        
        # Generate variants
        variant_a, bbox_a = self._create_variant_a(background.copy(), text)  # Slightly flawed
        variant_b, bbox_b = self._create_variant_b(background.copy(), text)  # Best
        variant_c, bbox_c = self._create_variant_c(background.copy(), text)  # Bad
        
        cv2.imwrite(str(sample_dir / "A.jpg"), variant_a, [cv2.IMWRITE_JPEG_QUALITY, 100])
        cv2.imwrite(str(sample_dir / "B.jpg"), variant_b, [cv2.IMWRITE_JPEG_QUALITY, 100])
        cv2.imwrite(str(sample_dir / "C.jpg"), variant_c, [cv2.IMWRITE_JPEG_QUALITY, 100])
        
        # Calculate difficulty
        difficulty = (index % 5) * 0.2  # 0.0 to 0.8

        issues_a = ['compression', 'blur']
        issues_c = ['heavy_blur', 'artifacts', 'color_shift']
        if self.enable_typography_artifacts:
            issues_a.extend(['font_mismatch', 'size_inconsistency', 'kerning_jitter'])
            issues_c.extend(['font_mismatch', 'size_inconsistency', 'kerning_jitter'])
        if self.enable_layout_artifacts:
            issues_a.extend(['alignment_drift', 'line_break_degradation'])
            issues_c.extend(['alignment_drift', 'line_break_degradation'])
        if self.enable_visual_artifacts:
            issues_a.extend(['contrast_mismatch', 'line_spacing_inconsistency'])
            issues_c.extend(['contrast_mismatch', 'line_spacing_inconsistency'])
        if self.enable_styling_artifacts:
            issues_a.append('missing_attribution_styling')
            issues_c.append('missing_attribution_styling')
        
        # Create metadata
        meta = {
            'sample_id': sample_name,
            'original_text': original_text,
            'difficulty': difficulty,
            'variants': {
                'A': {
                    'type': 'slightly_flawed',
                    'issues': issues_a
                },
                'B': {'type': 'best', 'quality_score': 0.95},
                'C': {
                    'type': 'bad',
                    'issues': issues_c
                }
            },
            'background_consistency': {
                'shared_source_background_across_group': True,
                'artifacts_restricted_to_text_bbox': True
            },
            'text_bboxes': {
                'input': [int(v) for v in input_bbox],
                'expected': [int(v) for v in expected_bbox],
                'A': [int(v) for v in bbox_a],
                'B': [int(v) for v in bbox_b],
                'C': [int(v) for v in bbox_c]
            },
            'created': datetime.now().isoformat()
        }
        
        # Save metadata
        with open(sample_dir / "meta.json", 'w') as f:
            json.dump(meta, f, indent=2)
        
        return meta
    
    def _create_variant_a(self, background: np.ndarray, text: str):
        """Create mild-degradation variant A and return `(image, text_bbox)`."""
        
        if self.enable_typography_artifacts or self.enable_layout_artifacts or self.enable_visual_artifacts or self.enable_styling_artifacts:
            # Mild typography/layout artifacts + slight blur
            img, text_bbox = self.renderer.multi_line_text_with_typography_artifacts(
                background,
                text,
                artifact_strength=self.typography_artifact_strength_a if self.enable_typography_artifacts else 0.0,
                layout_artifact_strength=self.layout_artifact_strength_a if self.enable_layout_artifacts else 0.0,
                visual_artifact_strength=self.visual_artifact_strength_a if self.enable_visual_artifacts else 0.0,
                styling_artifact_strength=self.styling_artifact_strength_a if self.enable_styling_artifacts else 0.0,
                return_bbox=True
            )
        else:
            img, text_bbox = self.renderer.multi_line_text(background, text, font_size=22, return_bbox=True)
        img = self._apply_gaussian_blur_in_bbox(img, text_bbox, (3, 3), 0)
        
        # Slight compression artifacts (text region only)
        img = self._apply_jpeg_artifacts_in_bbox(img, text_bbox, quality=75)
        
        return img, text_bbox
    
    def _create_variant_b(self, background: np.ndarray, text: str):
        """Create best-quality variant B and return `(image, text_bbox)`."""
        
        # Perfect rendering
        img, text_bbox = self.renderer.multi_line_text(background, text, font_size=22, return_bbox=True)
        
        # Slight enhancement (text region only)
        img = self._apply_luma_equalize_in_bbox(img, text_bbox)
        
        return img, text_bbox
    
    def _create_variant_c(self, background: np.ndarray, text: str):
        """Create strong-degradation variant C and return `(image, text_bbox)`."""
        
        if self.enable_typography_artifacts or self.enable_layout_artifacts or self.enable_visual_artifacts or self.enable_styling_artifacts:
            # Strong typography/layout artifacts + heavy blur
            img, text_bbox = self.renderer.multi_line_text_with_typography_artifacts(
                background,
                text,
                artifact_strength=self.typography_artifact_strength_c if self.enable_typography_artifacts else 0.0,
                layout_artifact_strength=self.layout_artifact_strength_c if self.enable_layout_artifacts else 0.0,
                visual_artifact_strength=self.visual_artifact_strength_c if self.enable_visual_artifacts else 0.0,
                styling_artifact_strength=self.styling_artifact_strength_c if self.enable_styling_artifacts else 0.0,
                return_bbox=True
            )
        else:
            img, text_bbox = self.renderer.multi_line_text(background, text, font_size=22, return_bbox=True)
        img = self._apply_gaussian_blur_in_bbox(img, text_bbox, (9, 9), 2)
        
        # Add noise (text region only)
        img = self._apply_noise_in_bbox(img, text_bbox, sigma=15.0)
        
        # Heavy compression (text region only)
        img = self._apply_jpeg_artifacts_in_bbox(img, text_bbox, quality=30)
        
        # Color shift (text region only)
        img = self._apply_color_shift_in_bbox(img, text_bbox, alpha=0.8, beta=20)
        
        return img, text_bbox
    
    def _create_manifest(self, samples: List[Dict]):
        """Write dataset-level manifest (`manifest.json`) for all samples."""
        
        manifest = {
            'name': self.dataset_name,
            'created': datetime.now().isoformat(),
            'total_samples': len(samples),
            'image_size': self.image_size,
            'samples': samples
        }
        
        with open(self.dataset_dir / "manifest.json", 'w') as f:
            json.dump(manifest, f, indent=2)


def _is_running_in_streamlit() -> bool:
    """Return True when this module is executed with `streamlit run`."""
    streamlit_flags = (
        "STREAMLIT_SERVER_PORT",
        "STREAMLIT_SERVER_HEADLESS",
        "STREAMLIT_BROWSER_GATHER_USAGE_STATS",
        "STREAMLIT_THEME_BASE",
    )
    if any(flag in os.environ for flag in streamlit_flags):
        return True

    return "streamlit" in (sys.argv[0] or "").lower()


def _render_streamlit_entrypoint_notice() -> None:
    """
    Show a non-blank helper UI when users run this core module with Streamlit.
    """
    import streamlit as st

    st.set_page_config(
        page_title="Auto Dataset Generator (Core)",
        page_icon="🎬",
        layout="centered"
    )

    st.title("Auto Dataset Generator")
    st.subheader("Core Engine Module")
    st.warning(
        "You launched `auto_dataset_generator.py`, which contains the backend "
        "generation engine. The interactive UI lives in `auto_dataset_streamlit.py`."
    )

    st.code("streamlit run auto_dataset_streamlit.py", language="bash")
    st.caption("Use the command above to open the full dataset generation interface.")

    st.divider()
    st.write("You can still use this module programmatically:")
    st.code(
        "from auto_dataset_generator import DatasetGenerator\n"
        "gen = DatasetGenerator(num_samples=100)\n"
        "dataset_path = gen.generate()\n"
        "print(dataset_path)",
        language="python"
    )


if __name__ == "__main__":
    if _is_running_in_streamlit():
        _render_streamlit_entrypoint_notice()
    else:
        print("This file is the core engine, not the UI.")
        print("Use: streamlit run auto_dataset_streamlit.py")
