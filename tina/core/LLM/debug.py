from llama_cpp import Llama
path = r"D:\wangchuri\development\project\tina\tina-sauce----tcgai\model\GGUF\bge-m3-q8_0.gguf"
embd = Llama(path,n_gpu_layers=-1)
output = embd(
	"Once upon a time,",
	max_tokens=512,
	echo=True
)
print(output)