#Install: pip install git+https://github.com/huggingface/transformers.git

#docs: https://huggingface.co/docs/transformers/model_doc/codegen
#source and data: https://github.com/salesforce/CodeGen
from sty import fg, bg
from generate import generate







# Code to load the demos.
print(
  f'{fg(0, 250, 255)}\nTHIS IS A DEMO running from a smaller dataset. {fg.rs}\nA larger dataset may provide better results.\nType {bg(0, 0, 0)+fg(255, 75, 100)}example {fg(255, 255, 0)}[file]{bg.rs+fg.rs} to complete a demo file.\nExample: {bg(0, 0, 0)+fg(255, 75, 100)}example {fg(255, 255, 0)}example.py{bg.rs+fg.rs}\n'
)


while True:
  cmd = input('$ ').split()
  
  if cmd[0] == 'example':
    with open('examples/' + cmd[1]) as f:
      output = generate(f.read())
      print("Output:\n", output['fullcode'], sep="")
      print(f"Generation took {output['time']} seconds.")
      
  if cmd[0] == 'complete':
    ouput = generate(' '.join(cmd[1:]))
    print("Output:\n", output['fullcode'], sep="")
    print(f"Generation took {output['time']} seconds.")
    
  if cmd[0] == 'help':
    print('$example [file] — Uses AI to autocomplete.\n$complete [code] — Autocompletes the inputted code.')