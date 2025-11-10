"""
Test script to verify the backend setup is working correctly
"""
import os
import sys
from pathlib import Path

def test_environment():
    """Test environment setup"""
    print("[*] Testing environment setup...")
    
    # Check for API key
    from dotenv import load_dotenv
    load_dotenv("cle.env")
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("[OK] API key found")
        print(f"     Key starts with: {api_key[:20]}...")
    else:
        print("[FAIL] API key not found in environment")
        return False
    
    return True

def test_data_loader():
    """Test data loader"""
    print("\n[*] Testing data loader...")
    
    try:
        from data_loader import DataLoader
        loader = DataLoader()
        
        print(f"[OK] Data loader initialized")
        print(f"     Text content: {len(loader.text_content)} characters")
        print(f"     Image folders: {list(loader.images_data.keys())}")
        
        total_images = sum(len(imgs) for imgs in loader.images_data.values())
        print(f"     Total images: {total_images}")
        
        if total_images == 0:
            print("[WARN] No images loaded - check image folder paths")
        
        return True
    except Exception as e:
        print(f"[FAIL] Error loading data: {e}")
        return False

def test_imports():
    """Test required imports"""
    print("\n[*] Testing imports...")
    
    required_packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("openai", "OpenAI"),
        ("pydantic", "Pydantic"),
    ]
    
    all_ok = True
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"[OK] {name} installed")
        except ImportError:
            print(f"[FAIL] {name} not installed")
            all_ok = False
    
    return all_ok

def test_file_structure():
    """Test file structure"""
    print("\n[*] Testing file structure...")
    
    required_files = [
        "../chatbot-extension/output_text.txt",
        "cle.env",
        "main.py",
        "data_loader.py"
    ]
    
    all_ok = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"[OK] {file_path} exists")
        else:
            print(f"[FAIL] {file_path} not found")
            all_ok = False
    
    # Check for image folders
    image_folders = [
        "../chatbot-extension/images_extraites",
        "../chatbot-extension/images_nommees",
        "../chatbot-extension/images_simples",
        "../chatbot-extension/images_titre_associe"
    ]
    
    for folder in image_folders:
        if Path(folder).exists():
            count = len(list(Path(folder).glob("*")))
            print(f"[OK] {folder} ({count} files)")
        else:
            print(f"[WARN] {folder} not found")
    
    return all_ok

def main():
    print("=" * 50)
    print("  L-mobile Chatbot Setup Verification")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Python Imports", test_imports),
        ("Environment", test_environment),
        ("Data Loader", test_data_loader),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n[FAIL] {test_name} failed with error: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("  Test Results Summary")
    print("=" * 50)
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} - {test_name}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n[SUCCESS] All tests passed! You're ready to start the server.")
        print("\nTo start the server, run:")
        print("  python main.py")
        print("\nOr use the startup script:")
        print("  start_server.bat (Windows)")
        print("  ./start_server.sh (Linux/Mac)")
    else:
        print("\n[WARNING] Some tests failed. Please fix the issues above.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

