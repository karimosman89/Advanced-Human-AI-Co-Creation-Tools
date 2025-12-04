"""
Creative Studio Demo: Complete Marketing Campaign Generation

This example demonstrates creating a comprehensive multi-channel marketing campaign
using the Multimodal Creator.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from co_creation_tools.creative_studio import MultimodalCreator
from co_creation_tools.creative_studio.multimodal_creator import Style


def main():
    """Run Creative Studio demo"""
    
    print("="*80)
    print("CREATIVE STUDIO DEMO: Marketing Campaign Generation")
    print("="*80)
    
    # Initialize Creative Studio
    print("\n🎨 Initializing Creative Studio...")
    creator = MultimodalCreator(workspace_dir="./demo_output")
    
    # Campaign details
    product_name = "AI-Powered Development Suite"
    target_audience = "Software developers and engineering teams"
    key_message = "Ship better code 10x faster with AI assistance"
    channels = ['social', 'email', 'web', 'ads']
    
    print(f"\n📢 Campaign Details:")
    print(f"   • Product: {product_name}")
    print(f"   • Audience: {target_audience}")
    print(f"   • Message: {key_message}")
    print(f"   • Channels: {', '.join(channels)}")
    
    # Create complete marketing campaign
    print("\n🚀 Generating comprehensive marketing campaign...")
    campaign = creator.create_marketing_campaign(
        product_name=product_name,
        target_audience=target_audience,
        key_message=key_message,
        channels=channels
    )
    
    # Display campaign summary
    print("\n" + "="*80)
    print("CAMPAIGN SUMMARY")
    print("="*80)
    
    summary = creator.get_project_summary(campaign.project_id)
    print(f"\n📊 Campaign Statistics:")
    print(f"   • Project ID: {summary['project_id']}")
    print(f"   • Total Assets: {summary['total_assets']}")
    print(f"   • Asset Types: {', '.join(summary['asset_breakdown'].keys())}")
    print(f"   • Created: {summary['created_at']}")
    
    # Display generated assets
    print("\n" + "="*80)
    print("GENERATED ASSETS")
    print("="*80)
    
    for i, asset in enumerate(campaign.assets, 1):
        print(f"\n{'─'*80}")
        print(f"Asset {i}: {asset['type'].upper()}")
        print(f"{'─'*80}")
        
        if asset['type'] == 'text':
            print(f"Prompt: {asset.get('prompt', 'N/A')}")
            print(f"Style: {asset.get('style', 'N/A')}")
            print(f"\nContent (Variation 1):")
            print(asset['variations'][0]['text'][:500] + "...")
            
        elif asset['type'] == 'image_prompt':
            print(f"Description: {asset.get('description', 'N/A')}")
            print(f"Style: {asset.get('style', 'N/A')}")
            print(f"Aspect Ratio: {asset.get('aspect_ratio', 'N/A')}")
            print(f"\nOptimized Prompt:")
            print(asset.get('optimized_prompt', 'N/A'))
    
    # Example: Generate additional content variations
    print("\n" + "="*80)
    print("GENERATING CONTENT VARIATIONS")
    print("="*80)
    
    print("\n📝 Generating product description in multiple styles...")
    
    styles_to_test = [
        (Style.MARKETING, "Marketing Style"),
        (Style.TECHNICAL, "Technical Style"),
        (Style.CREATIVE, "Creative Style")
    ]
    
    for style, style_name in styles_to_test:
        print(f"\n{'─'*80}")
        print(f"{style_name}")
        print(f"{'─'*80}")
        
        result = creator.generate_text(
            project_id=campaign.project_id,
            prompt=f"Product description for {product_name}",
            style=style,
            max_length=300
        )
        
        print(result['variations'][0]['text'][:300] + "...")
    
    # Export campaign
    print("\n" + "="*80)
    print("EXPORTING CAMPAIGN")
    print("="*80)
    
    print("\n💾 Exporting campaign to file...")
    export_path = creator.export_project(campaign.project_id, format="markdown")
    print(f"✅ Campaign exported to: {export_path}")
    
    # Additional example: Code generation
    print("\n" + "="*80)
    print("BONUS: CODE GENERATION")
    print("="*80)
    
    print("\n💻 Generating landing page code...")
    code_result = creator.generate_code(
        project_id=campaign.project_id,
        description="Landing page component with hero section and CTA",
        language="javascript",
        framework="React"
    )
    
    print(f"\n📄 Generated Code ({code_result['lines_of_code']} lines):")
    print(code_result['code'][:400] + "...")
    
    print("\n" + "="*80)
    print("✅ Demo completed successfully!")
    print(f"📁 All files saved in: ./demo_output/")
    print("="*80)


if __name__ == "__main__":
    main()
