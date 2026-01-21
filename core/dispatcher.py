from pyrogram import Client
from typing import Callable, List
import importlib
import os

class Dispatcher:
    """Handler dispatcher for organizing bot handlers"""
    
    def __init__(self, app: Client):
        self.app = app
        self.handlers: List[Callable] = []
    
    def register_handler(self, handler: Callable):
        """Register a handler function"""
        self.handlers.append(handler)
        print(f"✅ Registered handler: {handler.__name__}")
    
    def load_handlers_from_module(self, module_name: str):
        """Load all handlers from a module"""
        try:
            module = importlib.import_module(module_name)
            # Look for setup_handlers function in module
            if hasattr(module, 'setup_handlers'):
                module.setup_handlers(self.app)
                print(f"✅ Loaded handlers from {module_name}")
        except Exception as e:
            print(f"❌ Error loading handlers from {module_name}: {e}")
    
    def load_all_handlers(self):
        """Load all handlers from handlers directory"""
        handler_modules = [
            'handlers.start',
            'handlers.upload',
            'handlers.download',
            'handlers.links',
            'handlers.search',
            'handlers.user',
            'handlers.admin',
            'handlers.errors',
        ]
        
        for module_name in handler_modules:
            self.load_handlers_from_module(module_name)
        
        print("✅ All handlers loaded")
    
    def load_plugins(self):
        """Load optional plugins"""
        from config import config
        
        if config.ENABLE_SELF_DESTRUCT:
            try:
                from plugins.self_destruct import setup_plugin
                setup_plugin(self.app)
                print("✅ Self-destruct plugin loaded")
            except Exception as e:
                print(f"⚠️  Self-destruct plugin error: {e}")
        
        # Add more plugin loading here
        print("✅ Plugins loaded")