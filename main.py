# Webpy by Bernard
import socket
import os
import ssl
import threading
from urllib.parse import unquote
import traceback
from io import StringIO
import sys


def htmlfy(input):
    try:
        input = input.decode('utf-8')
        input = input.replace("Á", "&Acute;")
        input = input.replace("á", "&aacute;")
        input = input.replace("À", "&Agrave;")
        input = input.replace("à", "&agrave;")
        input = input.replace("Â", "&Acirc;")
        input = input.replace("â", "&acirc;")
        input = input.replace("Ã", "&Atilde;")
        input = input.replace("ã", "&atilde;")
        input = input.replace("ç", "&ccedil;")
        input = input.replace("Ç", "&Ccedil;")
        input = input.replace("É", "&Eacute;")
        input = input.replace("é", "&eacute;")
        input = input.replace("È", "&Egrave;")
        input = input.replace("Ê", "&Ecirc;")
        input = input.replace("ê", "&ecirc;")
        input = input.replace("Í", "&Iacute;")
        input = input.replace("í", "&iacute;")
        input = input.replace("Ì", "&Igrave;")
        input = input.replace("ì", "&igrave;")
        input = input.replace("Ó", "&Oacute;")
        input = input.replace("ó", "&oacute;")
        input = input.replace("Õ", "&Otilde;")
        input = input.replace("õ", "&otilde;")
        return input.encode()
    except:
        return input

class exceptions():
	class BindFail(Exception):
		pass
	class DecodeError(Exception):
		pass


def execute(code, _globals={}, _locals={}):
	fake_stdout = StringIO()
	__stdout = sys.stdout
	sys.stdout = fake_stdout
	try:
		ret = eval(code, _globals, _locals)
		result = fake_stdout.getvalue()
		sys.stdout = __stdout
		if ret:
			result += str(ret)
		return result
	except:
		try:
			exec(code, _globals, _locals)
		except:
			sys.stdout = __stdout			
			buf = StringIO()
			traceback.print_exc(file=buf)
			return buf.getvalue()
		else:
			sys.stdout = __stdout
			return fake_stdout.getvalue()


def pythonfier(contents, vars={}):
	code = contents
	cookie = ""
	code_lines = contents.replace("\n", "\\n").split("<python>")[1:]
	for code_line in code_lines:
		cd = code_line.split("</python>")[0].replace("\t", "•")		
		cut_size = 0
		for char in list(cd):
			if char in ["n", " ", "\\", "•"]:
				cut_size += 1
			else:
				break
		cd = code_line.split("</python>")[0].replace("•", " ")[cut_size:].replace("\\n", "\n")
		code_exec = execute(cd, _globals=vars)
		check = code_exec.split("⌠")
		if len(check) == 2:
			cookie = check[1]
			code_exec = check[0]		
		code = code.replace("<python>"+(code_line.split("</python>")[0]+"</python>").replace("\\n", "\n").replace("•", "\t"), code_exec)
	return cookie, code.encode()


class WebServer(object):
	def __init__(self, port, content_dir, host=None):
		self.port = port
		if not host: 
			self.host = socket.gethostbyname(socket.gethostname())
		else:
			self.host = host
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#Content dir treatment
		if content_dir.startswith("\\"): content_dir = content_dir[1:]
		if not content_dir.endswith("\\") and len(content_dir) > 0: content_dir += "\\"
		self.content_dir = content_dir
		
		#A masterpiece
		class events(object):
			def __init__(self):
				self.hooks = {"requests": [], "requests_handler": {}}
			def request_input(self, function):			
				self.hooks["requests"].append(function)
			def request_handler(self, type):
				def wrapper(function):		
					self.hooks["requests_handler"][type.upper()] = function
				return wrapper
		self.events = events()

	def _headers(self, status, cookie=""):
		preset = f"\nServer: Webpy\nConnection: close\n\n"
		if cookie != "":
			preset = f"\nServer: Webpy\nConnection: close\n{cookie}\n\n"
		if status == 200:
			header = "HTTP/1.1 200 Response OK" + preset
		elif status == 401:
			header = "HTTP/1.1 400 Not Authorized." + preset
		elif status == 403:
			header = "HTTP/1.1 403 Permissions Required." + preset
		elif status == 404:
			header = "HTTP/1.1 404 Not Found." + preset
		else:
			header = "HTTP/1.1 500 Server Could Not Process the Request." + preset
		return header

	def _request_handler(self, type, body, addr):
		cookies = ""
		vars = {"cookies": {}, "url_params": {}, "ip": addr}
		for line in body.split("\n"):
			if line.startswith("Cookie:"):
				cook = line[8:].split("; ")
				for cokizinho in cook:
					for cokizinho in cook:
						if cokizinho.endswith("\r"):
							vars["cookies"].update({cokizinho.split("=")[0]: cokizinho.split("=")[1][:-1]})
						else:
							vars["cookies"].update({cokizinho.split("=")[0]: cokizinho.split("=")[1]})
		
		try:
			for param in body.split(" ")[1].split("?")[1].split("&"):
				vars["url_params"].update({param.split("=")[0]: param.split("=")[1]})
		except:
			pass
		# Filename treatment

		file = body.split(" ")[1].split("?")[0]
		if file.startswith("/"):
			if len(file) == 1: file = "index.html"
			else:
				file = file[1:]
			file = self.content_dir + file.replace("/", "\\")
			if not file.endswith("\\") and os.path.isdir(file):
				if os.path.isdir(file+"\\"):
					file += "\\"
					return b"HTTP/1.1 302 Path Realocation\nConnection: Close\nLocation: "+file.replace("\\", "/").encode("utf-8")+b"\nServer: Stronghold Proxy\n\n"
			if os.path.isdir(file) and file.endswith("\\"):
				file += "\\index.html"
		
		for event_function in self.events.hooks["requests"]:
			event_function(type, body, addr, file, vars["cookies"])
		
		if type in self.events.hooks["requests_handler"]:
			return self.events.hooks["requests_handler"][type](type, body, addr, file, vars["cookies"], vars["url_params"])
		
		elif type in ["GET", "HEAD"]:
			try:
				file_contents = htmlfy(open(file, "rb").read())
				if file.endswith(".html"): cookies, file_contents = pythonfier(file_contents.decode(), vars)
				return self._headers(200, cookies).encode() + file_contents
			except FileNotFoundError:
				return self._headers(
					404).encode() + b"<html><head><title>404</title></head><body><center><h1>Erro 404</h1></center></body></html>"
			except OSError:
				return self._headers(403).encode() + htmlfy(
					f"<html><head><title>403</title></head><body><center><h1>Erro 403</h1><br><p>Esta p&aacutegina &eacute restrita.</p></center></body></html>").encode()
			except Exception as e:
				return self._headers(500).encode() + htmlfy(
					f"<html><head><title>500</title></head><body><center><h1>Erro 500</h1><br><p>Um erro occoreu no servidor. detalhes:<br>{e}</p></center></body></html>").encode()
		elif type == "POST":
			values = {"cookies": {}, "ip": addr}
			for line in body.split("\n"):
				if line.startswith("Cookie:"):
					cook = line[8:].split("; ")
					for cokizinho in cook:
						if cokizinho.endswith("\r"):
							values["cookies"].update({cokizinho.split("=")[0]: cokizinho.split("=")[1][:-1]})
						else:
							values["cookies"].update({cokizinho.split("=")[0]: cokizinho.split("=")[1]})
			try:
				for value in unquote(body.split("\n")[-1]).split("&"):
					values.update({value.split("=")[0]: value.split("=")[1]})
			except Exception as e:
				raise e
				exit(1)
			if file == self.content_dir + "/": file = self.content_dir + "index.html"
			try:
				file_contents = htmlfy(open(file, "rb").read())
				if file.endswith(".html"): cookies, file_contents = pythonfier(file_contents.decode("utf-8"), values)
				return self._headers(200, cookies).encode() + file_contents
			except FileNotFoundError:
				return self._headers(
					404).encode() + b"<html><head><title>404</title></head><body><center><h1>Erro 404</h1></center></body></html>"
			except OSError:
				return self._headers(403).encode() + htmlfy(
					f"<html><head><title>403</title></head><body><center><h1>Erro 403</h1><br><p>Esta p&aacutegina &eacute restrita.</p></center></body></html>".encode()).encode()
			except Exception as e:
				return self._headers(500).encode() + htmlfy(
					f"<html><head><title>500</title></head><body><center><h1>Erro 500</h1><br><p>Um erro occoreu no servidor. detalhes:<br>{e}</p></center></body></html>".encode()).encode()
		return self._headers(200).encode() + body.encode()

	def _handler(self, client, addr):
		while True:
			data = client.recv(1000024)
			if not data: break
			try:
				data = data.decode('utf-8')
			except Exception as e:
				client.close()
				for event_function in self.events.hooks["requests"]:
					event_function(None, data, addr, None, None)
				break
			method = data.split(" ")[0]
			response = self._request_handler(method, data, addr[0])
			client.send(response)
			client.close()	
			break

	def start(self):
		stop = False
		try:
			self.socket.bind((self.host, self.port))
		except Exception as e:
			self.socket.close()
			stop = True
		if stop: raise exceptions.BindFail()
		self._listener()

	def _listener(self):
		self.socket.listen(5)
		while True:
			(client, addr) = self.socket.accept()
			client.settimeout(60)
			threading.Thread(target=self._handler, args=(client, addr)).start()
