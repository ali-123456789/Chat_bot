"""
Data loader for chatbot - loads all images and text data
"""
import os
import base64
import json
from pathlib import Path
from typing import List, Dict

class DataLoader:
    def __init__(self, base_path: str = "../chatbot-extension"):
        self.base_path = Path(base_path)
        self.images_data = {}
        self.text_content = ""
        self.load_all_data()
    
    def load_all_data(self):
        """Load all images and text data"""
        print("[INFO] Loading data (text only)...")
        
        # Load text content
        self.load_text_content()
        
        # Skip image loading for now (faster startup)
        # self.load_images_from_folders()
        
        print(f"[OK] Text content loaded and ready")
    
    def load_text_content(self):
        """Load text from output_text.txt"""
        text_file = self.base_path / "output_text.txt"
        if text_file.exists():
            with open(text_file, "r", encoding="utf-8") as f:
                self.text_content = f.read()
            print(f"[OK] Loaded text content ({len(self.text_content)} characters)")
        else:
            print("[WARN] output_text.txt not found")
    
    def load_images_from_folders(self):
        """Load images from all image folders"""
        image_folders = [
            "images_extraites",
            "images_nommees", 
            "images_simples",
            "images_titre_associe"
        ]
        
        for folder in image_folders:
            folder_path = self.base_path / folder
            if folder_path.exists():
                images = self.load_images_from_folder(folder_path, folder)
                self.images_data[folder] = images
                print(f"[OK] Loaded {len(images)} images from {folder}")
            else:
                print(f"[WARN] Folder not found: {folder}")
    
    def load_images_from_folder(self, folder_path: Path, folder_name: str) -> List[Dict]:
        """Load all images from a specific folder"""
        images = []
        for img_file in folder_path.glob("*"):
            if img_file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.webp']:
                images.append({
                    "name": img_file.name,
                    "path": str(img_file),
                    "folder": folder_name,
                    "size": img_file.stat().st_size
                })
        return images
    
    def get_image_base64(self, image_path: str) -> str:
        """Convert image to base64 for OpenAI API"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return None
    
    def get_relevant_images(self, query: str, max_images: int = 3) -> List[Dict]:
        """Get relevant images based on query keywords"""
        # Simple keyword matching for now
        query_lower = query.lower()
        relevant_images = []
        
        # Search in images_nommees first (they have descriptive names)
        if "images_nommees" in self.images_data:
            for img in self.images_data["images_nommees"]:
                # Extract keywords from filename
                name_lower = img["name"].lower()
                if any(word in name_lower for word in query_lower.split() if len(word) > 3):
                    relevant_images.append(img)
                    if len(relevant_images) >= max_images:
                        return relevant_images
        
        # If not enough images found, add from other folders
        for folder in ["images_titre_associe", "images_simples"]:
            if folder in self.images_data and len(relevant_images) < max_images:
                for img in self.images_data[folder]:
                    name_lower = img["name"].lower()
                    if any(word in name_lower for word in query_lower.split() if len(word) > 3):
                        relevant_images.append(img)
                        if len(relevant_images) >= max_images:
                            return relevant_images
        
        return relevant_images
    
    def get_context_for_query(self, query: str, max_chars: int = 3000) -> str:
        """Extract relevant context from text based on query"""
        if not self.text_content:
            return ""
        
        query_lower = query.lower()
        lines = self.text_content.split('\n')
        
        # Find relevant sections
        relevant_lines = []
        context_window = 5  # lines before and after match
        
        for i, line in enumerate(lines):
            if any(word in line.lower() for word in query_lower.split() if len(word) > 3):
                # Add context around the match
                start = max(0, i - context_window)
                end = min(len(lines), i + context_window + 1)
                relevant_lines.extend(lines[start:end])
        
        # If no specific match, return first part of document
        if not relevant_lines:
            return '\n'.join(lines[:100])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_lines = []
        for line in relevant_lines:
            if line not in seen:
                seen.add(line)
                unique_lines.append(line)
        
        context = '\n'.join(unique_lines)
        
        # Limit size
        if len(context) > max_chars:
            context = context[:max_chars] + "..."
        
        return context
    
    def get_all_images_summary(self) -> Dict:
        """Get summary of all available images"""
        summary = {}
        for folder, images in self.images_data.items():
            summary[folder] = {
                "count": len(images),
                "sample_names": [img["name"] for img in images[:3]]
            }
        return summary

