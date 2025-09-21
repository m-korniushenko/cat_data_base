from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.enums import TA_CENTER
from datetime import datetime
import os


class CatPDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom styles for the PDF"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=20,
            spaceAfter=15,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        ))
        
        # Heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading1'],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=8,
            textColor=colors.darkblue
        ))
        
        # Subheading style
        self.styles.add(ParagraphStyle(
            name='CustomSubHeading',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=6,
            spaceBefore=6,
            textColor=colors.darkgreen
        ))
        
        # Normal text style
        self.styles.add(ParagraphStyle(
            name='CustomNormal',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=4
        ))
    
    def generate_cat_pdf(self, cat_info, family_tree, output_path):
        """Generate PDF with cat information and family tree"""
        doc = SimpleDocTemplate(output_path, pagesize=A4,
                                topMargin=0.5*inch, bottomMargin=0.5*inch,
                                leftMargin=0.5*inch, rightMargin=0.5*inch)
        story = []
        
        # Title
        title = Paragraph(
            f"🐱 {cat_info['cat'].cat_firstname} {cat_info['cat'].cat_surname}",
            self.styles['CustomTitle']
        )
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Create compact combined table with all information
        story.append(Paragraph("📋 Cat Information", self.styles['CustomHeading']))
        story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.darkblue))
        
        # Prepare data for compact table
        cat_data = [
            ['🐱 Basic Information', '', '', ''],
            ['Name:', f"{cat_info['cat'].cat_firstname} {cat_info['cat'].cat_surname}",
             'Callname:', cat_info['cat'].cat_callname or 'Not specified'],
            ['Gender:', cat_info['cat'].cat_gender,
             'Title:', cat_info['cat'].cat_title[0] if cat_info['cat'].cat_title else 'Not specified'],
            ['Birthday:', str(cat_info['cat'].cat_birthday),
             'Chip Number:', cat_info['cat'].cat_microchip_number or 'Not specified'],
            ['Studbook #1:', cat_info['cat'].cat_haritage_number or 'Not specified',
             'Studbook #2:', cat_info['cat'].cat_haritage_number_2 or 'Not specified'],
            ['Eye Color:', cat_info['cat'].cat_eye_colour or 'Not specified',
             'Hair Type:', cat_info['cat'].cat_hair_type or 'Not specified'],
            ['Color:', cat_info['cat'].cat_EMS_colour or 'Not specified',
             'Litter:', cat_info['cat'].cat_litter or 'Not specified'],
            ['Litter Size (M):', (str(cat_info['cat'].cat_litter_size_male)
                                 if cat_info['cat'].cat_litter_size_male else 'Not specified'),
             'Litter Size (F):', (str(cat_info['cat'].cat_litter_size_female) 
                                 if cat_info['cat'].cat_litter_size_female else 'Not specified')],
            
            ['🏥 Health Information', '', '', ''],
            ['Tests:', cat_info['cat'].cat_tests or 'Not specified',
             'Blood Group:', cat_info['cat'].cat_blood_group or 'Not specified'],
            ['Gencode:', cat_info['cat'].cat_gencode or 'Not specified',
             'Weight:', f"{cat_info['cat'].cat_weight} kg" if cat_info['cat'].cat_weight else 'Not specified'],
            ['Birth Weight:', (f"{cat_info['cat'].cat_birth_weight} g" 
                              if cat_info['cat'].cat_birth_weight else 'Not specified'),
             'Transfer Weight:', (f"{cat_info['cat'].cat_transfer_weight} g" 
                                if cat_info['cat'].cat_transfer_weight else 'Not specified')],
            ['Jaw Fault:', cat_info['cat'].cat_jaw_fault or 'Not specified',
             'Hernia:', cat_info['cat'].cat_hernia or 'Not specified'],
            ['Testicles:', cat_info['cat'].cat_testicles or 'Not specified',
             'Faults/Deviations:', cat_info['cat'].cat_faults_deviations or 'Not specified'],
            
            ['🐾 Breeding Information', '', '', ''],
            ['Breeding Lock:', 'Yes' if cat_info['cat'].cat_breeding_lock else 'No',
             'Breeding Lock Date:', (str(cat_info['cat'].cat_breeding_lock_date) 
                                    if cat_info['cat'].cat_breeding_lock_date else 'Not specified')],
            ['Breeding Animal:', 'Yes' if cat_info['cat'].cat_breeding_animal else 'No',
             'Kitten Transfer:', 'Yes' if cat_info['cat'].cat_kitten_transfer else 'No'],
            ['Birth Country:', cat_info['cat'].cat_birth_country or 'Not specified',
             'Location:', cat_info['cat'].cat_location or 'Not specified'],
            ['Association:', cat_info['cat'].cat_association or 'Not specified',
             '', ''],
            
            ['💀 Death Information', '', '', ''],
            ['Death Date:', str(cat_info['cat'].cat_death_date) if cat_info['cat'].cat_death_date else 'Not specified',
             'Death Cause:', cat_info['cat'].cat_death_cause or 'Not specified'],
            ['Status:', cat_info['cat'].cat_status or 'Not specified',
             '', ''],
            
            ['👤 Owner Information', '', '', ''],
            ['Name:', (f"{cat_info['owner'].owner_firstname} {cat_info['owner'].owner_surname}" 
                      if cat_info['owner'] else 'Not specified'),
             'Email:', cat_info['owner'].owner_email if cat_info['owner'] else 'Not specified'],
            ['Phone:', (cat_info['owner'].owner_phone or 'Not specified' 
                       if cat_info['owner'] else 'Not specified'),
             'Address:', (cat_info['owner'].owner_address or 'Not specified' 
                         if cat_info['owner'] else 'Not specified')],
            ['City:', (cat_info['owner'].owner_city or 'Not specified' 
                      if cat_info['owner'] else 'Not specified'),
             'Country:', (cat_info['owner'].owner_country or 'Not specified' 
                         if cat_info['owner'] else 'Not specified')],
            ['ZIP:', (cat_info['owner'].owner_zip or 'Not specified' 
                     if cat_info['owner'] else 'Not specified'),
             '', '']
        ]
        
        # Add breeder info if available
        if cat_info['breed']:
            cat_data.extend([
                ['🏭 Breeder Info', '', '', ''],
                ['Name:', f"{cat_info['breed'].breed_firstname} {cat_info['breed'].breed_surname}",
                 'Email:', cat_info['breed'].breed_email],
                ['Phone:', cat_info['breed'].breed_phone or 'Not specified',
                 'Address:', cat_info['breed'].breed_address or 'Not specified'],
                ['City:', cat_info['breed'].breed_city or 'Not specified',
                 'Country:', cat_info['breed'].breed_country or 'Not specified']
            ])
        
        # Add parents info
        if cat_info['dam'] or cat_info['sire']:
            cat_data.extend([
                ['👨‍👩‍👧‍👦 Parents Info', '', '', ''],
                ['Mother:', f"{cat_info['dam'].cat_firstname} {cat_info['dam'].cat_surname}" 
                 if cat_info['dam'] else 'Not specified',
                 'Father:', f"{cat_info['sire'].cat_firstname} {cat_info['sire'].cat_surname}" 
                 if cat_info['sire'] else 'Not specified'],
                ['M. Gender:', cat_info['dam'].cat_gender if cat_info['dam'] else 'Not specified',
                 'F. Gender:', cat_info['sire'].cat_gender if cat_info['sire'] else 'Not specified'],
                ['M. Birthday:', str(cat_info['dam'].cat_birthday) if cat_info['dam'] else 'Not specified',
                 'F. Birthday:', str(cat_info['sire'].cat_birthday) if cat_info['sire'] else 'Not specified'],
                ['M. Microchip:', cat_info['dam'].cat_microchip_number or 'Not specified' 
                 if cat_info['dam'] else 'Not specified',
                 'F. Microchip:', cat_info['sire'].cat_microchip_number or 'Not specified' 
                 if cat_info['sire'] else 'Not specified']
            ])
        
        compact_table = Table(cat_data, colWidths=[1.2*inch, 2.3*inch, 1.2*inch, 2.3*inch])
        compact_table.setStyle(TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            
            # Section headers styling
            ('BACKGROUND', (0, 1), (-1, 1), colors.lightblue),
            
            # General styling
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 1), (2, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
            ('FONTNAME', (3, 1), (3, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
            ('TOPPADDING', (0, 1), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        
        # Add conditional styling
        if cat_info['breed']:
            compact_table.setStyle(TableStyle([('BACKGROUND', (0, 8), (-1, 8), colors.lightgreen)]))
        
        if cat_info['dam'] or cat_info['sire']:
            compact_table.setStyle(TableStyle([('BACKGROUND', (0, 13), (-1, 13), colors.lightyellow)]))
        
        story.append(compact_table)
        story.append(Spacer(1, 15))
        
        # Additional Information section
        additional_info = []
        if cat_info['cat'].cat_features:
            additional_info.append(['Features:', cat_info['cat'].cat_features])
        if cat_info['cat'].cat_notes:
            additional_info.append(['Notes:', cat_info['cat'].cat_notes])
        if cat_info['cat'].cat_show_results:
            additional_info.append(['Show Results:', cat_info['cat'].cat_show_results])
        
        if additional_info:
            story.append(Paragraph("📝 Additional Information", self.styles['CustomHeading']))
            story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.darkblue))
            
            for info in additional_info:
                story.append(Paragraph(f"<b>{info[0]}</b>", self.styles['CustomSubHeading']))
                story.append(Paragraph(info[1], self.styles['Normal']))
                story.append(Spacer(1, 8))
            
            story.append(Spacer(1, 10))
        
        # Photos section
        if cat_info['cat'].cat_photos and len(cat_info['cat'].cat_photos) > 0:
            story.append(Paragraph("📸 Photos", self.styles['CustomHeading']))
            story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.darkblue))
            
            # Add photos in a grid layout
            photos = cat_info['cat'].cat_photos
            for i in range(0, len(photos), 2):  # 2 photos per row
                photo_row = []
                for j in range(2):
                    if i + j < len(photos):
                        photo_path = photos[i + j]
                        # Normalize path separators for file system check
                        normalized_path = photo_path.replace('/', '\\') if os.name == 'nt' else photo_path
                        if os.path.exists(normalized_path):
                            try:
                                # Create image with max size constraints
                                img = Image(normalized_path, width=2*inch, height=2*inch)
                                img.hAlign = 'CENTER'
                                photo_row.append(img)
                            except Exception:
                                # If image can't be loaded, add text instead
                                photo_row.append(Paragraph(f"Photo {i+j+1}<br/>(Error loading)", 
                                                          self.styles['Normal']))
                        else:
                            photo_row.append(Paragraph(f"Photo {i+j+1}<br/>(File not found)", self.styles['Normal']))
                    else:
                        photo_row.append(Paragraph("", self.styles['Normal']))
                
                if photo_row:
                    photo_table = Table([photo_row], colWidths=[2.5*inch, 2.5*inch])
                    photo_table.setStyle(TableStyle([
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ]))
                    story.append(photo_table)
                    story.append(Spacer(1, 8))
            
            story.append(Spacer(1, 10))
        
        # Files section
        if cat_info['cat'].cat_files and len(cat_info['cat'].cat_files) > 0:
            story.append(Paragraph("📁 Files", self.styles['CustomHeading']))
            story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.darkblue))
            
            # Add files list
            files = cat_info['cat'].cat_files
            for i, file_path in enumerate(files):
                try:
                    if file_path:
                        # Get filename from path and extract original name
                        full_filename = os.path.basename(file_path)
                        # Remove UUID part to show original filename
                        if '_' in full_filename:
                            parts = full_filename.split('_')
                            if len(parts) >= 2:
                                # Check if last part looks like UUID (8 hex characters)
                                last_part = parts[-1]
                                file_ext = os.path.splitext(last_part)[1]
                                uuid_part = last_part.replace(file_ext, '')
                                if len(uuid_part) == 8 and all(c in '0123456789abcdef' for c in uuid_part.lower()):
                                    # Remove the UUID part and rejoin
                                    original_name = '_'.join(parts[:-1]) + file_ext
                                else:
                                    original_name = full_filename
                            else:
                                original_name = full_filename
                        else:
                            original_name = full_filename
                        
                        # Normalize path separators for file system check
                        normalized_path = file_path.replace('/', '\\') if os.name == 'nt' else file_path
                        if os.path.exists(normalized_path):
                            story.append(Paragraph(f"📎 {original_name}", self.styles['Normal']))
                        else:
                            story.append(Paragraph(f"📎 {original_name} (File not found)", self.styles['Normal']))
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")
                    story.append(Paragraph(f"📎 {file_path} (Error processing)", self.styles['Normal']))
            
            story.append(Spacer(1, 10))
        
        # Family Tree - Compact version
        story.append(Spacer(1, 10))
        story.append(Paragraph("🌳 Family Tree", self.styles['CustomHeading']))
        story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.darkgreen))
        
        if family_tree:
            # Generate compact family tree table
            try:
                family_data = self.generate_family_tree_table(family_tree)
                if family_data and len(family_data) > 0:
                    family_table = Table(family_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
                    family_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                        
                        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 1), (-1, -1), 8),
                        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                        ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
                        ('TOPPADDING', (0, 1), (-1, -1), 3),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey)
                    ]))
                    
                    story.append(family_table)
                else:
                    # No family tree data available
                    story.append(Paragraph("No family tree information available.", self.styles['Normal']))
            except Exception as e:
                print(f"Error generating family tree table: {e}")
                story.append(Paragraph("Error generating family tree information.", self.styles['Normal']))
        else:
            # No family tree data available
            story.append(Paragraph("No family tree information available.", self.styles['Normal']))
        
        # Footer
        story.append(Spacer(1, 30))
        story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.grey))
        story.append(Paragraph(
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            self.styles['CustomNormal']
        ))
        
        # Build PDF
        doc.build(story)
    
    def generate_family_tree_table(self, family_tree, max_depth=3):
        """Generate compact table representation of family tree"""
        if not family_tree:
            return []
        
        # Collect all family members by generation
        generations = {}
        
        def collect_generation(node, depth=0):
            if not node or depth > max_depth:
                return
            
            # Check if node has required fields
            if not isinstance(node, dict) or 'firstname' not in node or 'surname' not in node:
                return
            
            if depth not in generations:
                generations[depth] = []
            
            generations[depth].append({
                'name': f"{node.get('firstname', 'Unknown')} {node.get('surname', 'Unknown')}",
                'gender': node.get('gender', 'Unknown'),
                'birthday': str(node.get('birthday', 'Unknown')),
                'microchip': node.get('microchip') or 'N/A'
            })
            
            if node.get('dam'):
                collect_generation(node['dam'], depth + 1)
            if node.get('sire'):
                collect_generation(node['sire'], depth + 1)
        
        collect_generation(family_tree)
        
        # Create table data
        table_data = []
        
        # Headers
        headers = ['Generation 1', 'Generation 2', 'Generation 3', 'Generation 4']
        table_data.append(headers)
        
        # Fill data by generation
        if not generations:
            return []
        
        max_rows = max(len(generations.get(i, [])) for i in range(max_depth + 1))
        
        for row in range(max_rows):
            row_data = []
            for gen in range(max_depth + 1):
                if gen in generations and row < len(generations[gen]):
                    cat = generations[gen][row]
                    row_data.append(f"{cat['name']}\n({cat['gender']})\n{cat['birthday']}")
                else:
                    row_data.append('')
            table_data.append(row_data)
        
        return table_data
    
    def generate_family_tree_text(self, family_tree, depth=0, max_depth=5):
        """Generate text representation of family tree"""
        if not family_tree or depth > max_depth:
            return ""
        
        indent = "  " * depth
        result = f"{indent}• {family_tree['firstname']} {family_tree['surname']} ({family_tree['gender']}) - {family_tree['birthday']}\n"
        
        if family_tree.get('dam'):
            result += f"{indent}  Mother:\n"
            result += self.generate_family_tree_text(family_tree['dam'], depth + 2, max_depth)
        
        if family_tree.get('sire'):
            result += f"{indent}  Father:\n"
            result += self.generate_family_tree_text(family_tree['sire'], depth + 2, max_depth)
        
        return result


def generate_cat_pdf_file(cat_info, family_tree, filename=None):
    """Generate PDF file for a cat"""
    if not filename:
        cat_name = f"{cat_info['cat'].cat_firstname}_{cat_info['cat'].cat_surname}".replace(" ", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cat_profile_{cat_name}_{timestamp}.pdf"
    
    # Create output directory if it doesn't exist
    output_dir = "generated_pdfs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_path = os.path.join(output_dir, filename)
    
    generator = CatPDFGenerator()
    generator.generate_cat_pdf(cat_info, family_tree, output_path)
    
    return output_path, filename
