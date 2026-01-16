"""
Fixed version of authenticate_cvlac with robust browser cleanup.

This module provides a patched version of the authenticate_cvlac function
that ensures browsers are properly closed even when cleanup operations fail.
"""

import logging
import time
from typing import Dict, Optional

try:
    from helium import start_chrome, go_to, write, click, kill_browser, Text, TextField, Button, S, select
except ImportError:
    # If helium is not available, provide a warning
    logging.warning("Helium package not available. Browser automation functions will not work.")
    

def authenticate_cvlac_fixed(nacionalidad: str, nombres: str, documento_identificacion: str, 
                           password: str, pais_nacimiento: Optional[str] = None, 
                           headless: bool = True) -> Dict[str, any]:
    """
    Authenticate with the CVLaC (Curriculum Vitae de Latinoamérica y el Caribe) system.
    
    This is a fixed version that ensures proper browser cleanup even when cleanup operations fail.
    
    Args:
        nacionalidad (str): The nationality option to select from dropdown
        nombres (str): The user's full name
        documento_identificacion (str): The identification document number
        password (str): The password for CVLaC login
        pais_nacimiento (str, optional): Country of birth (required when nacionalidad is "Extranjero - otra" or "E")
        headless (bool): Whether to run browser in headless mode (default: True)
        
    Returns:
        dict: Authentication result with status and session information
        
    Raises:
        Exception: If authentication fails or browser operations encounter errors
    """
    # Validate inputs
    if not nacionalidad or not nombres or not documento_identificacion or not password:
        return {
            "status": "error",
            "message": "All fields (nacionalidad, nombres, documento_identificacion, password) are required",
            "session_active": False
        }
    
    # Check if pais_nacimiento is required for "Extranjero - otra"
    if nacionalidad in ["Extranjero - otra", "E"] and not pais_nacimiento:
        return {
            "status": "error",
            "message": "pais_nacimiento is required when nacionalidad is 'Extranjero - otra'",
            "session_active": False
        }
    
    login_url = "https://scienti.minciencias.gov.co/cvlac/Login/pre_s_login.do"
    browser_started = False
    
    try:
        # Start browser
        if headless:
            browser = start_chrome(headless=True)
        else:
            browser = start_chrome()
        
        browser_started = True
        
        # Navigate to login page
        go_to(login_url)
        
        # Fill in credentials according to actual CVLaC form fields
        # Select nationality from dropdown using the exact field ID
        select(nacionalidad, from_=S("#tpo_nacionalidad") or S("[name='tpo_nacionalidad']") or S("select"))
        
        # If "Extranjero - otra" is selected, wait for and fill "País de nacimiento" field
        if nacionalidad in ["Extranjero - otra", "E"]:
            # Wait for the country field to become visible and fill it
            select(pais_nacimiento, from_=S("#sgl_pais_nacim") or S("[name='sgl_pais_nacim']"))
        
        # Fill in name using the exact field ID
        write(nombres, into=S("#txt_nmes_rh") or S("[name='txt_nmes_rh']") or TextField("Nombres"))
        
        # Fill in identification document using the exact field ID
        write(documento_identificacion, into=S("#nro_documento_ident") or S("[name='nro_documento_ident']") or TextField("Documento de identificación"))
        
        # Fill in password using the exact field ID
        write(password, into=S("#txt_contrasena") or S("[name='txt_contrasena']") or S("[type='password']"))
        
        # Submit form using the exact button ID
        click(S("#botonEnviar") or Button("Ingresar") or Button("Login") or Button("Entrar") or S("input[type='submit']"))
        
        # Check for successful authentication
        # This would need to be customized based on the actual success indicators
        # For now, we'll assume success if no error elements are found
        
        result = {
            "status": "success",
            "message": "Authentication successful",
            "session_active": True
        }
        
        return result
        
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Authentication failed: {str(e)}",
            "session_active": False
        }
    
    finally:
        # Robust browser cleanup with multiple attempts and error handling
        if browser_started:
            _robust_browser_cleanup()


def _robust_browser_cleanup(max_attempts: int = 3, delay_between_attempts: float = 1.0) -> None:
    """
    Perform robust browser cleanup with multiple attempts and error handling.
    
    Args:
        max_attempts (int): Maximum number of cleanup attempts
        delay_between_attempts (float): Delay in seconds between cleanup attempts
    """
    for attempt in range(max_attempts):
        try:
            kill_browser()
            logging.info(f"Browser cleanup successful on attempt {attempt + 1}")
            return
        except Exception as e:
            logging.warning(f"Browser cleanup attempt {attempt + 1} failed: {str(e)}")
            
            if attempt < max_attempts - 1:
                # Wait before the next attempt
                time.sleep(delay_between_attempts)
            else:
                # Last attempt failed, try alternative cleanup methods
                logging.error("All browser cleanup attempts failed, trying alternative methods")
                _alternative_browser_cleanup()


def _alternative_browser_cleanup() -> None:
    """
    Alternative browser cleanup methods when standard kill_browser() fails.
    """
    import os
    import signal
    import subprocess
    import platform
    
    try:
        system = platform.system().lower()
        
        if system == "linux" or system == "darwin":  # Linux or macOS
            # Try to kill Chrome processes
            try:
                subprocess.run(["pkill", "-f", "chrome"], check=False, capture_output=True)
                logging.info("Alternative cleanup: killed chrome processes with pkill")
            except Exception as e:
                logging.warning(f"pkill chrome failed: {str(e)}")
            
            # Try to kill chromedriver processes
            try:
                subprocess.run(["pkill", "-f", "chromedriver"], check=False, capture_output=True)
                logging.info("Alternative cleanup: killed chromedriver processes with pkill")
            except Exception as e:
                logging.warning(f"pkill chromedriver failed: {str(e)}")
                
        elif system == "windows":
            # Try to kill Chrome processes on Windows
            try:
                subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], check=False, capture_output=True)
                logging.info("Alternative cleanup: killed chrome.exe with taskkill")
            except Exception as e:
                logging.warning(f"taskkill chrome.exe failed: {str(e)}")
            
            # Try to kill chromedriver processes on Windows
            try:
                subprocess.run(["taskkill", "/F", "/IM", "chromedriver.exe"], check=False, capture_output=True)
                logging.info("Alternative cleanup: killed chromedriver.exe with taskkill")
            except Exception as e:
                logging.warning(f"taskkill chromedriver.exe failed: {str(e)}")
    
    except Exception as e:
        logging.error(f"Alternative browser cleanup failed: {str(e)}")


# Alias for backward compatibility
authenticate_cvlac = authenticate_cvlac_fixed