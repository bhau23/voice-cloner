#!/usr/bin/env python3
"""
✅ Project Verification and Status Script for Bhavesh AI Voice Cloner

This script performs a comprehensive check of the project to ensure
everything is properly set up and ready for deployment.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
import importlib.util

class ProjectVerifier:
    def __init__(self):
        self.checks_passed = 0
        self.checks_total = 0
        self.warnings = []
        self.errors = []
        
    def check(self, description, condition, warning=None, error=None):
        """Perform a verification check"""
        self.checks_total += 1
        print(f"🔍 {description}...", end=" ")
        
        if condition:
            print("✅")
            self.checks_passed += 1
            return True
        else:
            print("❌")
            if error:
                self.errors.append(error)
            elif warning:
                self.warnings.append(warning)
            return False
    
    def check_file_exists(self, filepath, description=None):
        """Check if a file exists"""
        if description is None:
            description = f"Checking {filepath}"
        return self.check(
            description, 
            Path(filepath).exists(),
            error=f"Missing file: {filepath}"
        )
    
    def check_directory_structure(self):
        """Verify project directory structure"""
        print("\n📁 Directory Structure")
        print("-" * 40)
        
        required_files = [
            "README.md",
            "requirements.txt", 
            "streamlit_app.py",
            "launch.py",
            "github_setup.py",
            "pyproject.toml",
            "setup.py",
            ".gitignore",
            "LICENSE"
        ]
        
        for file in required_files:
            self.check_file_exists(file)
        
        required_dirs = [
            "src/bhavesh_ai_voice_cloner",
            ".streamlit",
            ".github/workflows",
            "docs"
        ]
        
        for dir_path in required_dirs:
            self.check(
                f"Directory {dir_path}",
                Path(dir_path).is_dir(),
                error=f"Missing directory: {dir_path}"
            )
        
        # Check source files
        source_files = [
            "src/bhavesh_ai_voice_cloner/__init__.py",
            "src/bhavesh_ai_voice_cloner/tts.py",
            "src/bhavesh_ai_voice_cloner/vc.py"
        ]
        
        for file in source_files:
            self.check_file_exists(file, f"Source file {file}")
    
    def check_git_setup(self):
        """Verify Git configuration"""
        print("\n🔧 Git Configuration")
        print("-" * 40)
        
        # Check if Git is initialized
        self.check(
            "Git repository initialized",
            Path(".git").exists(),
            error="Git repository not initialized. Run: git init"
        )
        
        # Check Git config
        try:
            result = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True)
            self.check(
                "Git user name configured",
                result.returncode == 0 and result.stdout.strip(),
                error="Git user name not set. Run: git config user.name 'Your Name'"
            )
        except FileNotFoundError:
            self.check("Git installed", False, error="Git not found in PATH")
        
        try:
            result = subprocess.run(["git", "config", "user.email"], capture_output=True, text=True)
            self.check(
                "Git user email configured",
                result.returncode == 0 and result.stdout.strip(),
                error="Git user email not set. Run: git config user.email 'your@email.com'"
            )
        except FileNotFoundError:
            pass
        
        # Check for remote
        try:
            result = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True)
            has_remote = result.returncode == 0 and "origin" in result.stdout
            self.check(
                "Git remote origin configured",
                has_remote,
                warning="No Git remote configured. Run github_setup.py to set up GitHub"
            )
        except FileNotFoundError:
            pass
    
    def check_dependencies(self):
        """Check Python dependencies"""
        print("\n📦 Dependencies")
        print("-" * 40)
        
        # Check Python version
        python_version = sys.version_info
        self.check(
            "Python 3.9+",
            python_version >= (3, 9),
            error=f"Python 3.9+ required, found {python_version.major}.{python_version.minor}"
        )
        
        # Check requirements.txt
        if Path("requirements.txt").exists():
            with open("requirements.txt") as f:
                requirements = f.read().splitlines()
            
            critical_packages = [
                "streamlit", "torch", "torchaudio", "transformers", 
                "librosa", "numpy", "plotly", "pandas"
            ]
            
            for package in critical_packages:
                found = any(package in req for req in requirements)
                self.check(
                    f"Package {package} in requirements",
                    found,
                    warning=f"Package {package} not found in requirements.txt"
                )
        
        # Try importing critical modules
        critical_imports = [
            ("streamlit", "Streamlit"),
            ("torch", "PyTorch"),
            ("librosa", "Librosa"),
            ("plotly", "Plotly")
        ]
        
        for module_name, display_name in critical_imports:
            try:
                importlib.import_module(module_name)
                self.check(f"{display_name} importable", True)
            except ImportError:
                self.check(
                    f"{display_name} importable", 
                    False,
                    warning=f"{display_name} not installed. Run: pip install -r requirements.txt"
                )
    
    def check_package_structure(self):
        """Verify package structure and imports"""
        print("\n🐍 Package Structure")
        print("-" * 40)
        
        # Check if package can be imported
        try:
            sys.path.insert(0, "src")
            import bhavesh_ai_voice_cloner
            self.check("Package importable", True)
            
            # Check main classes
            try:
                from bhavesh_ai_voice_cloner.tts import BhaveshTTS
                self.check("BhaveshTTS class importable", True)
            except ImportError as e:
                self.check("BhaveshTTS class importable", False, error=str(e))
            
            try:
                from bhavesh_ai_voice_cloner.vc import BhaveshVC
                self.check("BhaveshVC class importable", True)
            except ImportError as e:
                self.check("BhaveshVC class importable", False, error=str(e))
                
        except ImportError as e:
            self.check("Package importable", False, error=str(e))
    
    def check_documentation(self):
        """Verify documentation completeness"""
        print("\n📚 Documentation")
        print("-" * 40)
        
        # Check README content
        if Path("README.md").exists():
            with open("README.md") as f:
                readme_content = f.read()
            
            required_sections = [
                "Bhavesh AI", "Installation", "Usage", "Features", 
                "License", "Contributing"
            ]
            
            for section in required_sections:
                self.check(
                    f"README contains {section}",
                    section.lower() in readme_content.lower(),
                    warning=f"README should mention {section}"
                )
        
        # Check other documentation
        docs = [
            ("CONTRIBUTING.md", "Contributing guidelines"),
            ("STREAMLIT_DEPLOYMENT.md", "Streamlit deployment guide"),
            ("LICENSE", "License file")
        ]
        
        for filepath, description in docs:
            self.check_file_exists(filepath, description)
    
    def check_deployment_readiness(self):
        """Check if project is ready for deployment"""
        print("\n🚀 Deployment Readiness")
        print("-" * 40)
        
        # Check Streamlit config
        self.check_file_exists(".streamlit/config.toml", "Streamlit configuration")
        
        # Check GitHub Actions
        self.check_file_exists(".github/workflows/ci.yml", "GitHub Actions CI")
        
        # Check Docker files
        self.check_file_exists("Dockerfile", "Docker configuration")
        self.check_file_exists("docker-compose.yml", "Docker Compose configuration")
        
        # Check if streamlit app runs (basic syntax check)
        try:
            with open("streamlit_app.py") as f:
                code = f.read()
            compile(code, "streamlit_app.py", "exec")
            self.check("Streamlit app syntax valid", True)
        except SyntaxError as e:
            self.check("Streamlit app syntax valid", False, error=f"Syntax error: {e}")
        except Exception as e:
            self.check("Streamlit app readable", False, error=str(e))
    
    def check_branding(self):
        """Verify rebranding is complete"""
        print("\n🎨 Branding")
        print("-" * 40)
        
        # Check for old references
        files_to_check = ["README.md", "pyproject.toml", "setup.py"]
        old_terms = ["chatterbox", "resemble", "ResembleAI"]
        new_terms = ["bhavesh", "Bhavesh AI"]
        
        for filepath in files_to_check:
            if Path(filepath).exists():
                with open(filepath, encoding='utf-8') as f:
                    content = f.read().lower()
                
                # Check for old terms (should be minimal/none)
                old_found = any(term.lower() in content for term in old_terms)
                if old_found:
                    self.warnings.append(f"Old branding terms found in {filepath}")
                
                # Check for new terms (should be present)
                new_found = any(term.lower() in content for term in new_terms)
                self.check(
                    f"Bhavesh AI branding in {filepath}",
                    new_found,
                    warning=f"Bhavesh AI branding should be in {filepath}"
                )
    
    def generate_report(self):
        """Generate final verification report"""
        print("\n" + "=" * 60)
        print("📊 VERIFICATION REPORT")
        print("=" * 60)
        
        success_rate = (self.checks_passed / self.checks_total) * 100 if self.checks_total > 0 else 0
        
        print(f"✅ Checks Passed: {self.checks_passed}/{self.checks_total} ({success_rate:.1f}%)")
        
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"   • {error}")
        
        print(f"\n🎯 Project Status:")
        if success_rate >= 90:
            print("   🎉 EXCELLENT - Ready for production deployment!")
        elif success_rate >= 75:
            print("   ✅ GOOD - Ready for deployment with minor fixes")
        elif success_rate >= 50:
            print("   ⚠️  NEEDS WORK - Several issues need addressing")
        else:
            print("   ❌ NOT READY - Major issues need fixing")
        
        print(f"\n📋 Next Steps:")
        if success_rate >= 90:
            print("   1. Run: python github_setup.py")
            print("   2. Deploy to Streamlit Cloud")
            print("   3. Share your project!")
        else:
            print("   1. Fix the errors listed above")
            print("   2. Run this verification again")
            print("   3. Consult documentation for help")
        
        return success_rate >= 75

def main():
    print("🎤 BHAVESH AI VOICE CLONER - Project Verification")
    print("=" * 60)
    print("This script will verify that your project is properly set up")
    print("and ready for deployment.\n")
    
    verifier = ProjectVerifier()
    
    # Run all checks
    verifier.check_directory_structure()
    verifier.check_git_setup()
    verifier.check_dependencies()
    verifier.check_package_structure()
    verifier.check_documentation()
    verifier.check_deployment_readiness()
    verifier.check_branding()
    
    # Generate report
    is_ready = verifier.generate_report()
    
    return 0 if is_ready else 1

if __name__ == "__main__":
    sys.exit(main())
