# coding=utf-8
import io
from datetime import datetime
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from fastapi import HTTPException, status

from models import Paciente, ReporteExportado
from services.paciente_service import PacienteService

class ReporteService:
    @staticmethod
    def generar_pdf_paciente(db: Session, paciente_id: int, usuario_id: int) -> io.BytesIO:
        # Obtener datos
        paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
        if not paciente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado")
        
        historial = PacienteService.obtener_historial_paciente(db, paciente_id)
        
        # Iniciar documento en memoria
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        title_style.alignment = 1 # Center
        subtitle_style = styles['Heading2']
        normal_style = styles['Normal']
        
        custom_bold = ParagraphStyle(
            'CustomBold',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            spaceAfter=6
        )
        
        elements = []
        
        # Título
        elements.append(Paragraph(f"Reporte Clínico TICOS NurseDx", title_style))
        elements.append(Spacer(1, 20))
        
        # Datos del Paciente
        elements.append(Paragraph("Datos del Paciente", subtitle_style))
        
        datos_paciente = [
            ["Nombre Completo:", paciente.nombre_completo],
            ["Historia Clínica:", paciente.numero_historia],
            ["Documento:", f"{paciente.tipo_documento.upper()} {paciente.numero_documento}"],
            ["Fecha Reporte:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        ]
        
        t_paciente = Table(datos_paciente, colWidths=[120, 300])
        t_paciente.setStyle(TableStyle([
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ]))
        elements.append(t_paciente)
        elements.append(Spacer(1, 20))
        
        # Historial (Diagnósticos y Notas)
        elements.append(Paragraph("Historial Clínico y Diagnósticos NANDA", subtitle_style))
        elements.append(Spacer(1, 10))
        
        if not historial:
            elements.append(Paragraph("No hay registros en el historial para este paciente.", normal_style))
        else:
            for evento in historial:
                fecha_str = evento['fecha'].strftime("%Y-%m-%d %H:%M")
                usuario_str = evento['usuario']['nombre_completo'] if evento['usuario'] else "Desconocido"
                
                if evento['tipo'] == 'diagnostico':
                    metadata = evento.get('metadata', {})
                    nanda_codigo = metadata.get('codigo_nanda', '')
                    nanda_nombre = metadata.get('nombre_nanda', '')
                    header = f"<b>[{fecha_str}] Diagnóstico NANDA Asignado</b> - <i>por {usuario_str}</i>"
                    elements.append(Paragraph(header, normal_style))
                    elements.append(Paragraph(f"<b>Código:</b> {nanda_codigo} - {nanda_nombre}", normal_style))
                    if evento['detalle']:
                        elements.append(Paragraph(f"<b>Resultado esperado/Detalle:</b> {evento['detalle']}", normal_style))
                
                elif evento['tipo'] == 'nota':
                    header = f"<b>[{fecha_str}] Nota de Enfermería</b> - <i>por {usuario_str}</i>"
                    elements.append(Paragraph(header, normal_style))
                    elements.append(Paragraph(f"{evento['detalle']}", normal_style))
                
                elements.append(Spacer(1, 15))
        
        # Construir PDF
        doc.build(elements)
        buffer.seek(0)
        
        # Registrar exportación en base de datos
        nombre_archivo = f"reporte_paciente_{paciente.numero_documento}_{datetime.now().strftime('%Y%m%d%H%M')}.pdf"
        reporte = ReporteExportado(
            usuario_id=usuario_id,
            paciente_id=paciente.id,
            nombre_archivo=nombre_archivo
        )
        db.add(reporte)
        db.commit()
        
        return buffer, nombre_archivo

    @staticmethod
    def obtener_historial_exportaciones(db: Session, limit: int = 100):
        return db.query(ReporteExportado).order_by(ReporteExportado.generado_en.desc()).limit(limit).all()
