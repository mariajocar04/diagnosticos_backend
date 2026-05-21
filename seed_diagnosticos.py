# coding=utf-8
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Asegurar que se encuentra en la ruta del backend
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from database import DATABASE_URL
from models import NandaCatalogo

def seed_diagnosticos():
    load_dotenv()
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    print("Insertando registros de diagnósticos NANDA...")

    diagnosticos_data = [
        {"codigo": "00292", "nombre": "Disposición para mejorar la autogestión de la salud", "sintomas": "interés en aprender,voluntad de cambiar hábitos,confianza en las habilidades,preocupación por el bienestar", "intervenciones_nic": "Fomentar la autoeducación sobre la autogestión.,Establecer metas de salud específicas y alcanzables.,Brindar recursos educativos sobre autocuidado.,Proporcionar apoyo continuo para motivar la autogestión.", "resultados_noc": "Autogestión de la salud,Conocimiento sobre la salud"},
        {"codigo": "00162", "nombre": "Disposición para mejorar el estilo de vida", "sintomas": "reconocimiento de malos hábitos,deseo de mejorar la calidad de vida,falta de energía,estrés o ansiedad", "intervenciones_nic": "Proponer un plan de acción gradual para cambiar hábitos poco saludables.,Fomentar la educación sobre nutrición y ejercicio.,Ayudar a establecer metas alcanzables en términos de actividad física y dieta.,Proporcionar seguimiento y ajustes según el progreso del paciente.", "resultados_noc": "Mejora de la salud,Autocuidado"},
        {"codigo": "00161", "nombre": "Disposición para mejorar el conocimiento", "sintomas": "búsqueda activa de información,actitud abierta hacia nuevas ideas,aceptación de nuevas prácticas de salud", "intervenciones_nic": "Proporcionar materiales educativos accesibles y comprensibles.,Organizar talleres interactivos para mejorar la comprensión sobre la salud.,Fomentar la participación en grupos educativos de salud.,Evaluar la comprensión del paciente y ajustar las intervenciones educativas.", "resultados_noc": "Conocimiento sobre la salud,Participación en la educación para la salud"},
        {"codigo": "00078", "nombre": "Manejo ineficaz de la salud", "sintomas": "no adherencia a los regímenes terapéuticos,dificultad para reconocer cambios en el estado de salud,desorganización en el manejo de condiciones crónicas", "intervenciones_nic": "Proporcionar educación continua sobre la importancia del tratamiento.,Establecer un plan de seguimiento para el manejo de la salud.,Asegurar que el paciente comprenda y se adhiera a su plan de tratamiento.,Brindar apoyo emocional y motivacional para el autocuidado.", "resultados_noc": "Manejo de la salud,Autogestión de la salud"},
        {"codigo": "00168", "nombre": "Disposición para mejorar el manejo de la salud", "sintomas": "deseo de mejorar las habilidades de autogestión,interés por cambiar conductas relacionadas con la salud,actitud positiva hacia el cambio", "intervenciones_nic": "Fomentar la autoeficacia mediante el refuerzo positivo.,Establecer metas de salud alcanzables a corto y largo plazo.,Proponer intervenciones personalizadas para mejorar el manejo de la salud.,Proporcionar herramientas para el autocontrol de condiciones de salud.", "resultados_noc": "Manejo de la salud,Autogestión de la salud"},
        {"codigo": "00167", "nombre": "Autogestión ineficaz", "sintomas": "desorganización en el manejo de la salud,dificultad para seguir pautas de autocuidado,falta de control sobre condiciones crónicas", "intervenciones_nic": "Proponer un plan de autogestión individualizado.,Brindar formación continua sobre la autogestión.,Utilizar herramientas como recordatorios o aplicaciones de salud para seguimiento.,Proporcionar apoyo constante para mejorar la adherencia al tratamiento.", "resultados_noc": "Autogestión de la salud,Conocimiento sobre la salud"},
        {"codigo": "00244", "nombre": "Disposición para mejorar la autogestión", "sintomas": "motivación para mejorar el control de la salud,actitud positiva hacia la adopción de hábitos saludables,interés en aprender sobre la autogestión", "intervenciones_nic": "Fomentar la reflexión sobre las metas de autogestión de salud.,Proponer estrategias y metas a corto y largo plazo.,Establecer un plan detallado para la mejora de la autogestión.,Reforzar el empoderamiento del paciente con la toma de decisiones.", "resultados_noc": "Autogestión de la salud,Conocimiento sobre la salud"},
        {"codigo": "00001", "nombre": "Nutrición desequilibrada: más de lo que el cuerpo necesita", "sintomas": "aumento de peso,obesidad,fatiga,hipertensión,dolor de cabeza", "intervenciones_nic": "Proponer un plan de alimentación balanceado.,Fomentar la actividad física regular.,Monitorear el peso y la ingesta calórica.,Ofrecer educación sobre control de porciones y elección de alimentos saludables.", "resultados_noc": "Equilibrio nutricional,Control de peso"},
        {"codigo": "00002", "nombre": "Nutrición desequilibrada: menos de lo que el cuerpo necesita", "sintomas": "pérdida de peso,desnutrición,fatiga extrema,mareos,falta de concentración", "intervenciones_nic": "Aumentar la ingesta de alimentos ricos en nutrientes.,Proponer suplementos nutricionales.,Evaluar y tratar las deficiencias nutricionales.,Fomentar la hidratación adecuada.", "resultados_noc": "Equilibrio nutricional,Ingesta de alimentos"},
        {"codigo": "00163", "nombre": "Disposición para mejorar la nutrición", "sintomas": "deseo de mejorar la dieta,actitud positiva hacia los cambios alimenticios,falta de apetito", "intervenciones_nic": "Crear un plan nutricional personalizado.,Proveer recursos educativos sobre nutrición.,Monitorear la ingesta nutricional y ajustar el plan.,Establecer metas de nutrición a corto y largo plazo.", "resultados_noc": "Equilibrio nutricional,Control de peso"},
        {"codigo": "00134", "nombre": "Náuseas", "sintomas": "sensación de malestar estomacal,ganas de vomitar,pérdida de apetito", "intervenciones_nic": "Administrar medicamentos antieméticos.,Ofrecer líquidos claros y comidas suaves.,Evitar olores fuertes y alimentos irritantes.", "resultados_noc": "Reducción de las náuseas,Confort gastrointestinal"},
        {"codigo": "00255", "nombre": "Riesgo de náuseas", "sintomas": "historia de náuseas recurrentes,uso de medicamentos que causan náuseas", "intervenciones_nic": "Monitorear signos de náuseas.,Proponer una dieta ligera y evitar alimentos irritantes.,Administrar medicamentos preventivos.", "resultados_noc": "Reducción de las náuseas,Confort gastrointestinal"},
        {"codigo": "00013", "nombre": "Diarrea", "sintomas": "evacuaciones líquidas,dolor abdominal,urgencia para defecar", "intervenciones_nic": "Rehidratar al paciente.,Monitorear la frecuencia de evacuaciones.,Implementar una dieta baja en fibra y suave.", "resultados_noc": "Equilibrio de líquidos,Confort gastrointestinal"},
        {"codigo": "00196", "nombre": "Deterioro de la absorción gastrointestinal", "sintomas": "pérdida de peso no explicada,deficiencias nutricionales,síntomas de desnutrición", "intervenciones_nic": "Proporcionar suplementos nutricionales.,Evaluar la función gastrointestinal y el tratamiento.,Proponer cambios en la dieta para mejorar la absorción.", "resultados_noc": "Absorción gastrointestinal,Estado nutricional"},
        {"codigo": "00195", "nombre": "Riesgo de desequilibrio electrolítico", "sintomas": "fatiga,debilidad muscular,cambios en la presión arterial", "intervenciones_nic": "Monitorear los niveles de electrolitos.,Administrar suplementos de electrolitos.,Fomentar la hidratación adecuada.", "resultados_noc": "Equilibrio de líquidos,Balance electrolítico"},
        {"codigo": "00270", "nombre": "Riesgo de desequilibrio nutricional", "sintomas": "dieta inadecuada,pérdida de peso,malnutrición", "intervenciones_nic": "Implementar un plan nutricional adecuado.,Proporcionar educación sobre hábitos alimenticios saludables.,Monitorear la ingesta nutricional.", "resultados_noc": "Equilibrio nutricional,Estado nutricional"},
        {"codigo": "00020", "nombre": "Incontinencia urinaria de urgencia", "sintomas": "urgencia para orinar,pérdida involuntaria de orina,frecuencia urinaria aumentada", "intervenciones_nic": "Entrenamiento de la vejiga.,Uso de medicamentos anticolinérgicos.,Ejercicios de Kegel.", "resultados_noc": "Control de la micción,Confort urinario"},
        {"codigo": "00017", "nombre": "Incontinencia urinaria de esfuerzo", "sintomas": "pérdida de orina al toser o reír,sensación de incomodidad durante el esfuerzo físico", "intervenciones_nic": "Ejercicios de Kegel.,Uso de dispositivos absorbentes.,Terapia quirúrgica si es necesario.", "resultados_noc": "Control de la micción,Confort urinario"},
        {"codigo": "00015", "nombre": "Riesgo de deterioro de la eliminación urinaria", "sintomas": "alteración en el patrón de micción,dificultad para vaciar completamente la vejiga", "intervenciones_nic": "Monitorear la cantidad de orina y la función renal.,Fomentar el vaciamiento completo de la vejiga.,Ofrecer educación sobre la importancia de la hidratación.", "resultados_noc": "Control de la micción,Confort urinario"},
        {"codigo": "00011", "nombre": "Estreñimiento", "sintomas": "defecación infrecuente,dolor abdominal,distensión,sensación de evacuación incompleta", "intervenciones_nic": "Aumentar la ingesta de fibra y líquidos.,Fomentar la actividad física regular.,Administrar laxantes suaves si es necesario.", "resultados_noc": "Eliminación fecal,Confort gastrointestinal"},
        {"codigo": "00014", "nombre": "Incontinencia fecal", "sintomas": "pérdida involuntaria de heces,incapacidad para controlar evacuaciones", "intervenciones_nic": "Establecer una rutina de evacuación.,Administrar medicamentos para mejorar la consistencia de las heces.,Utilizar dispositivos absorbentes para control.", "resultados_noc": "Control de la eliminación fecal,Confort gastrointestinal"},
        {"codigo": "00030", "nombre": "Intercambio gaseoso deteriorado", "sintomas": "dificultad para respirar,cianosis,fatiga", "intervenciones_nic": "Administrar oxígeno suplementario.,Monitorear los niveles de oxígeno en sangre.,Fomentar técnicas de respiración controlada.", "resultados_noc": "Intercambio gaseoso,Oxigenación"},
        {"codigo": "00031", "nombre": "Limpieza ineficaz de las vías respiratorias", "sintomas": "dificultad para expectorar,tos persistente,respiración ruidosa", "intervenciones_nic": "Fomentar la tos productiva.,Administrar medicamentos mucolíticos.,Realizar fisioterapia respiratoria.", "resultados_noc": "Eliminación de secreciones respiratorias,Capacidad respiratoria"},
        {"codigo": "00039", "nombre": "Riesgo de aspiración", "sintomas": "dificultad para tragar,historia de atragantamientos", "intervenciones_nic": "Modificar la dieta a líquidos espesos o alimentos triturados.,Posicionar adecuadamente al paciente durante y después de comer.,Monitorear signos de aspiración durante la ingesta.", "resultados_noc": "Riesgo de aspiración,Seguridad respiratoria"},
        {"codigo": "00179", "nombre": "Autogestión ineficaz de la diabetes", "sintomas": "descontrol en los niveles de glucosa,dificultad para seguir el régimen de medicación o dieta,desconocimiento de las complicaciones de la diabetes", "intervenciones_nic": "Brindar educación sobre la diabetes y su manejo.,Fomentar el control regular de los niveles de glucosa.,Proponer cambios en la dieta que favorezcan el control de la glucosa.,Ayudar al paciente a establecer un plan de ejercicio adecuado.", "resultados_noc": "Manejo de la diabetes,Autogestión de la salud"},
    ]

    for data in diagnosticos_data:
        # Verificar si ya existe para evitar duplicados
        existing = db.query(NandaCatalogo).filter(NandaCatalogo.codigo == data["codigo"]).first()
        if not existing:
            nuevo = NandaCatalogo(
                codigo=data["codigo"],
                nombre=data["nombre"],
                sintomas=data["sintomas"],
                intervenciones_nic=data["intervenciones_nic"],
                resultados_noc=data["resultados_noc"]
            )
            db.add(nuevo)
            print(f"Agregado: {data['codigo']} - {data['nombre']}")
        else:
            print(f"Saltado (ya existe): {data['codigo']}")

    try:
        db.commit()
        print("\n¡Registros de catálogo NANDA insertados exitosamente!")
    except Exception as e:
        db.rollback()
        print(f"Error al insertar registros: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_diagnosticos()
