# AST Resume Automation Compliance Workflow

This GitHub workflow ensures your resume website is optimized for Applicant Tracking Systems (ATS) through automated compliance checks.

## What This Workflow Does

### 🔍 **Automated Compliance Checks**
- **HTML Structure Validation**: Ensures proper semantic markup and heading hierarchy
- **Required Sections**: Validates presence of essential resume sections (contact, experience, education, skills)
- **Contact Information**: Verifies email, phone, and professional profiles are properly formatted
- **Accessibility Compliance**: Checks for proper language attributes, character encoding, and viewport settings
- **Keyword Optimization**: Analyzes content for relevant data analytics industry keywords
- **ATS-Friendly Formatting**: Validates structure for optimal ATS parsing

### 📄 **PDF Generation**
- Automatically generates PDF versions of all pages
- Optimized formatting for ATS submission
- Professional A4 layout with appropriate margins

### 📊 **Detailed Reporting**
- Comprehensive compliance reports with pass/fail status
- Specific recommendations for improvements
- Progress tracking with pass rate calculations

## Workflow Triggers

The workflow runs automatically on:
- **Push to main/develop branches**
- **Pull requests to main branch**

## Compliance Standards

### Main Resume Page (index.html)
- ✅ Contact information (email, phone, LinkedIn)
- ✅ Professional experience section
- ✅ Education background
- ✅ Technical skills
- ✅ Single H1 heading with proper hierarchy
- ✅ Data analytics keywords

### Career Goals Page
- ✅ Contact information
- ✅ Short-term and long-term goals
- ✅ Professional objectives

### Cover Letter Page
- ✅ Professional qualifications
- ✅ Career aspirations
- ✅ Value proposition

## Generated Artifacts

After each workflow run, the following artifacts are available for download:

1. **PDF Versions**: ATS-ready PDF files for all pages
2. **Compliance Report**: Detailed analysis results
3. **Built Site**: Complete Jekyll site with all assets

## Understanding the Results

### ✅ **Passed Checks**
Requirements that meet ATS compliance standards

### ⚠️ **Warnings**
Items that should be improved but don't prevent ATS processing

### ❌ **Errors**
Critical issues that may prevent proper ATS parsing

## Minimum Requirements

For the workflow to pass:
- **No critical errors**
- **Pass rate ≥ 70%**
- **All required sections present**
- **Valid contact information**

## Benefits for Job Applications

1. **ATS Compatibility**: Ensures your resume passes automated screening
2. **Professional Formatting**: Consistent, clean presentation
3. **Keyword Optimization**: Improved visibility for relevant searches
4. **Accessibility**: Better experience for all users
5. **Multi-Format Support**: Both web and PDF versions available

## Customization

To modify the compliance criteria:
1. Edit `.github/scripts/ast-compliance-check.py`
2. Adjust required sections, keywords, or validation rules
3. Update pass rate thresholds as needed

## Troubleshooting

Common issues and solutions:

**Heading Hierarchy Warnings**: Ensure single H1 per page with logical H2/H3 structure
**Missing Sections**: Add required content or update validation rules for specialized pages
**Contact Information Errors**: Verify proper formatting of email, phone, and profile links
**Low Keyword Coverage**: Include more industry-relevant terms naturally in content

## Support

This workflow is designed to help optimize your resume for modern hiring processes while maintaining professional presentation standards.