#!/usr/bin/env python3
import os
import re
import json
import sys
from pathlib import Path
import subprocess

class ASTComplianceChecker:
    def __init__(self, site_dir="_site"):
        self.site_dir = site_dir
        self.errors = []
        self.warnings = []
        self.passed_checks = []

    def log_error(self, check, message):
        self.errors.append(f"❌ {check}: {message}")

    def log_warning(self, check, message):
        self.warnings.append(f"⚠️  {check}: {message}")

    def log_pass(self, check, message):
        self.passed_checks.append(f"✅ {check}: {message}")

    def check_required_sections(self, html_content, filename):
        """Check for required resume sections"""
        # Different requirements for different page types
        if 'career-goals' in filename:
            # Career goals page requirements
            required_sections = {
                'contact': [r'contact', r'email', r'phone', r'linkedin'],
                'goals': [r'goals', r'roadmap', r'objectives', r'vision']
            }
        elif 'cover-letter' in filename:
            # Cover letter page requirements
            required_sections = {
                'qualifications': [r'qualified', r'experience', r'skills'],
                'aspirations': [r'aspirations', r'career', r'seeking']
            }
        else:
            # Main resume page requirements
            required_sections = {
                'contact': [r'contact', r'email', r'phone', r'linkedin'],
                'experience': [r'experience', r'work', r'employment'],
                'education': [r'education', r'degree', r'university', r'college'],
                'skills': [r'skills', r'technical', r'competenc']
            }
        
        for section, patterns in required_sections.items():
            found = any(re.search(pattern, html_content, re.IGNORECASE) for pattern in patterns)
            if found:
                self.log_pass(f"Required Section ({filename})", f"{section.title()} section found")
            else:
                self.log_error(f"Required Section ({filename})", f"{section.title()} section missing")

    def check_heading_hierarchy(self, html_content, filename):
        """Check proper heading hierarchy for ATS readability"""
        h1_count = len(re.findall(r'<h1[^>]*>', html_content, re.IGNORECASE))
        h2_matches = re.findall(r'<h2[^>]*>(.*?)</h2>', html_content, re.IGNORECASE | re.DOTALL)
        h3_matches = re.findall(r'<h3[^>]*>(.*?)</h3>', html_content, re.IGNORECASE | re.DOTALL)
        
        if h1_count == 1:
            self.log_pass(f"Heading Hierarchy ({filename})", "Single H1 tag found")
        elif h1_count == 0:
            self.log_error(f"Heading Hierarchy ({filename})", "No H1 tag found")
        else:
            self.log_warning(f"Heading Hierarchy ({filename})", f"Multiple H1 tags found: {h1_count}")
        
        if len(h2_matches) > 0:
            self.log_pass(f"Heading Hierarchy ({filename})", f"H2 sections found: {len(h2_matches)}")
        else:
            self.log_warning(f"Heading Hierarchy ({filename})", "No H2 sections found")

    def check_contact_information(self, html_content, filename):
        """Validate contact information presence and format"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\d{10})'
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        github_pattern = r'github\.com/[\w-]+'
        
        # Check email for all pages
        if re.search(email_pattern, html_content):
            self.log_pass(f"Contact Info ({filename})", "Email address found")
        else:
            # Only require email on main resume and career-goals pages
            if 'cover-letter' not in filename:
                self.log_error(f"Contact Info ({filename})", "No valid email address found")
            else:
                self.log_warning(f"Contact Info ({filename})", "No email address found")
        
        # Check phone (less critical for cover letter and career goals)
        if re.search(phone_pattern, html_content):
            self.log_pass(f"Contact Info ({filename})", "Phone number found")
        else:
            if filename == 'index.html':
                self.log_warning(f"Contact Info ({filename})", "No phone number found")
        
        # Check LinkedIn (beneficial for all pages)
        if re.search(linkedin_pattern, html_content):
            self.log_pass(f"Contact Info ({filename})", "LinkedIn profile found")
        else:
            if filename == 'index.html':
                self.log_warning(f"Contact Info ({filename})", "No LinkedIn profile found")

    def check_semantic_markup(self, html_content, filename):
        """Check for proper semantic HTML structure"""
        semantic_tags = ['<header', '<main', '<section', '<article', '<nav', '<footer']
        found_tags = []
        
        for tag in semantic_tags:
            if tag in html_content.lower():
                found_tags.append(tag.strip('<'))
        
        if len(found_tags) >= 3:
            self.log_pass(f"Semantic Markup ({filename})", f"Good semantic structure: {', '.join(found_tags)}")
        else:
            self.log_warning(f"Semantic Markup ({filename})", f"Limited semantic tags: {', '.join(found_tags)}")

    def check_accessibility_features(self, html_content, filename):
        """Check basic accessibility features"""
        has_lang = 'lang=' in html_content
        has_alt_attrs = 'alt=' in html_content
        has_meta_charset = 'charset=' in html_content
        has_viewport = 'viewport' in html_content
        
        if has_lang:
            self.log_pass(f"Accessibility ({filename})", "Language attribute found")
        else:
            self.log_error(f"Accessibility ({filename})", "Missing language attribute")
        
        if has_meta_charset:
            self.log_pass(f"Accessibility ({filename})", "Character encoding specified")
        else:
            self.log_error(f"Accessibility ({filename})", "Missing character encoding")
        
        if has_viewport:
            self.log_pass(f"Accessibility ({filename})", "Viewport meta tag found")
        else:
            self.log_warning(f"Accessibility ({filename})", "Missing viewport meta tag")

    def check_keyword_optimization(self, html_content, filename):
        """Check for relevant keywords for data analytics roles"""
        data_analytics_keywords = [
            'data', 'analytics', 'analysis', 'sql', 'python', 'tableau', 'excel',
            'statistics', 'visualization', 'database', 'reporting', 'dashboard',
            'machine learning', 'ml', 'business intelligence', 'bi', 'etl'
        ]
        
        content_lower = html_content.lower()
        found_keywords = [kw for kw in data_analytics_keywords if kw in content_lower]
        
        if len(found_keywords) >= 5:
            self.log_pass(f"Keywords ({filename})", f"Good keyword coverage: {len(found_keywords)} found")
        elif len(found_keywords) >= 3:
            self.log_warning(f"Keywords ({filename})", f"Moderate keyword coverage: {len(found_keywords)} found")
        else:
            self.log_error(f"Keywords ({filename})", f"Poor keyword coverage: {len(found_keywords)} found")

    def run_compliance_checks(self):
        """Run all AST compliance checks"""
        print("🔍 Running AST Resume Automation Compliance Checks...\n")
        
        html_files = list(Path(self.site_dir).rglob("*.html"))
        
        if not html_files:
            self.log_error("File Check", f"No HTML files found in {self.site_dir}")
            return False
        
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                filename = str(html_file.relative_to(Path(self.site_dir)))
                print(f"📄 Checking {filename}...")
                
                self.check_required_sections(content, filename)
                self.check_heading_hierarchy(content, filename)
                self.check_contact_information(content, filename)
                self.check_semantic_markup(content, filename)
                self.check_accessibility_features(content, filename)
                self.check_keyword_optimization(content, filename)
                
            except Exception as e:
                self.log_error("File Processing", f"Error processing {html_file}: {str(e)}")
        
        return self.print_results()

    def print_results(self):
        """Print compliance check results"""
        print("\n" + "="*60)
        print("AST COMPLIANCE CHECK RESULTS")
        print("="*60)
        
        print(f"\n✅ PASSED CHECKS ({len(self.passed_checks)}):")
        for check in self.passed_checks:
            print(f"  {check}")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  {warning}")
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  {error}")
        
        total_checks = len(self.passed_checks) + len(self.warnings) + len(self.errors)
        pass_rate = (len(self.passed_checks) / total_checks * 100) if total_checks > 0 else 0
        
        print(f"\n📊 SUMMARY:")
        print(f"  Total Checks: {total_checks}")
        print(f"  Passed: {len(self.passed_checks)}")
        print(f"  Warnings: {len(self.warnings)}")
        print(f"  Errors: {len(self.errors)}")
        print(f"  Pass Rate: {pass_rate:.1f}%")
        
        # Return True if no critical errors and pass rate > 70%
        return len(self.errors) == 0 and pass_rate >= 70.0

if __name__ == "__main__":
    checker = ASTComplianceChecker()
    success = checker.run_compliance_checks()
    sys.exit(0 if success else 1)