"""
Clase base para todas las skills de Ray Agent.
"""


class Skill:
    """Clase base abstracta para skills."""
    name: str = "base"
    description: str = "Skill base"

    def execute(self) -> dict:
        """
        Ejecuta la skill.
        Retorna: { "success": bool, "message": str, "data": any }
        """
        raise NotImplementedError(f"Skill '{self.name}' no implementó execute()")
