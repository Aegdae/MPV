from datetime import datetime

def time_since_creation(created_at):
            if isinstance(created_at, str): 
                created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")

            now = datetime.now()
            delta = now - created_at

            if delta.days > 0:
                return f"{delta.days} dias atrás"
            
            elif delta.seconds >= 3600:
                hours = delta.seconds // 3600
                return f"{hours} hr"
            
            elif delta.seconds >= 60: 
                minutes = delta.seconds // 60
                return f"{minutes} min"
            
            else:
                  return "Agora mesmo"