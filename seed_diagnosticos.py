# coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Diagnostico, Base
from database import DATABASE_URL

def seed_diagnosticos():
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    print("Insertando registros de diagnósticos NANDA...")

    diagnosticos_data = [
        {"codigo": "00292", "nombre": "Disposición para mejorar la autogestión de la salud", "sintomas": "interés en aprender,voluntad de cambiar hábitos,confianza en las habilidades,preocupación por el bienestar", "intervenciones_nic": "Fomentar la autoeducación sobre la autogestión.,Establecer metas de salud específicas y alcanzables.,Brindar recursos educativos sobre autocuidado.,Proporcionar apoyo continuo para motivar la autogestión.", "resultados_noc": "Autogestión de la salud,Conocimiento sobre la salud"},
        {"codigo": "00162", "nombre": "Disposición para mejorar el estilo de vida", "sintomas": "reconocimiento de malos hábitos,deseo de mejorar la calidad de vida,falta de energía,estrés o ansiedad", "intervenciones_nic": "Proponer un plan de acción gradual para cambiar hábitos poco saludables.,Fomentar la educación sobre nutrición y ejercicio.,Ayudar a establecer metas alcanzables en términos de actividad física y dieta.,Proporcionar seguimiento y ajustes según el progreso del paciente.", "resultados_noc": "Mejora de la salud,Autocuidado"},
        {"codigo": "00161", "nombre": "Disposición para mejorar el conocimiento", "sintomas": "búsqueda activa de información,actitud abierta hacia nuevas ideas,aceptación de nuevas prácticas de salud", "intervenciones_nic": "Proporcionar materiales educativos accesibles y comprensibles.,Organizar talleres interactivos para mejorar la comprensión sobre la salud.,Fomentar la participación en grupos educativos de salud.,Evaluar la comprensión del paciente y ajustar las intervenciones educativas.", "resultados_noc": "Conocimiento sobre la salud,Participación en la educación para la salud"},
        {"codigo": "00078", "nombre": "Manejo ineficaz de la salud", "sintomas": "no adherencia a los regímenes terapéuticos,dificultad para reconocer cambios en el estado de salud,desorganización en el manejo de condiciones crónicas", "intervenciones_nic": "Proporcionar educación continua sobre la importancia del tratamiento.,Establecer un plan de seguimiento para el manejo de la salud.,Asegurar que el paciente comprenda y se adhiera a su plan de tratamiento.,Brindar apoyo emocional y motivacional para el autocuidado.", "resultados_noc": "Manejo de la salud,Autogestión de la salud"},
        {"codigo": "00179", "nombre": "Autogestión ineficaz de la diabetes", "sintomas": "descontrol en los niveles de glucosa,dificultad para seguir el régimen de medicación o dieta,desconocimiento de las complicaciones de la diabetes", "intervenciones_nic": "Brindar educación sobre la diabetes y su manejo.,Fomentar el control regular de los niveles de glucosa.,Proponer cambios en la dieta que favorezcan el control de la glucosa.,Ayudar al paciente a establecer un plan de ejercicio adecuado.", "resultados_noc": "Manejo de la diabetes,Autogestión de la salud"},
        {"codigo": "00001", "nombre": "Nutrición desequilibrada: más de lo que el cuerpo necesita", "sintomas": "aumento de peso,obesidad,fatiga,hipertensión,dolor de cabeza", "intervenciones_nic": "Proponer un plan de alimentación balanceado.,Fomentar la actividad física regular.,Monitorear el peso y la ingesta calórica.,Ofrecer educación sobre control de porciones y elección de alimentos saludables.", "resultados_noc": "Equilibrio nutricional,Control de peso"},
        {"codigo": "00002", "nombre": "Nutrición desequilibrada: menos de lo que el cuerpo necesita", "sintomas": "pérdida de peso,desnutrición,fatiga extrema,mareos,falta de concentración", "intervenciones_nic": "Aumentar la ingesta de alimentos ricos en nutrientes.,Proponer suplementos nutricionales.,Evaluar y tratar las deficiencias nutricionales.,Fomentar la hidratación adecuada.", "resultados_noc": "Equilibrio nutricional,Ingesta de alimentos"},
        {"codigo": "00030", "nombre": "Intercambio gaseoso deteriorado", "sintomas": "dificultad para respirar,cianosis,fatiga", "intervenciones_nic": "Administrar oxígeno suplementario.,Monitorear los niveles de oxígeno en sangre.,Fomentar técnicas de respiración controlada.", "resultados_noc": "Intercambio gaseoso,Oxigenación"},
        {"codigo": "00031", "nombre": "Limpieza ineficaz de las vías respiratorias", "sintomas": "dificultad para expectorar,tos persistente,respiración ruidosa", "intervenciones_nic": "Fomentar la tos productiva.,Administrar medicamentos mucolíticos.,Realizar fisioterapia respiratoria.", "resultados_noc": "Eliminación de secreciones respiratorias,Capacidad respiratoria"},
        {"codigo": "00011", "nombre": "Estreñimiento", "sintomas": "defecación infrecuente,dolor abdominal,distensión,sensación de evacuación incompleta", "intervenciones_nic": "Aumentar la ingesta de fibra y líquidos.,Fomentar la actividad física regular.,Administrar laxantes suaves si es necesario.", "resultados_noc": "Eliminación fecal,Confort gastrointestinal"},
    ]

    for data in diagnosticos_data:
        # Verificar si ya existe para evitar duplicados
        existing = db.query(Diagnostico).filter(Diagnostico.codigo == data["codigo"]).first()
        if not existing:
            nuevo = Diagnostico(
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
        print("\n¡Registros de diagnósticos insertados exitosamente!")
    except Exception as e:
        db.rollback()
        print(f"Error al insertar registros: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_diagnosticos()
