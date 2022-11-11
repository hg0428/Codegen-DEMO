import time

print("Loading...")
startLoad = time.time()
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

GenerationLength = 300  #Max length
checkpoint = "Salesforce/codegen-350M-nl"  #ONLY USE #350M or it runs out of room. nl mode trains it from english. multi for a combination of languages. mono for just python. nl is the best one in my testing

model = AutoModelForCausalLM.from_pretrained(checkpoint)
#https://huggingface.co/docs/transformers/v4.23.1/en/main_classes/model#transformers.PreTrainedModel.from_pretrained
#https://pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

#model.train(True) #Puts it in training mode.
print(f"Initial model load complete in {time.time()-startLoad:.2f} seconds.")
print("Starting generation...")


#https://huggingface.co/docs/transformers/v4.23.1/en/main_classes/tokenizer#transformers.PreTrainedTokenizer
def generate(text):
  start = time.time()
  inputs = tokenizer(
    text,
    return_tensors="pt",
    max_length=len(text) + 1,  #Maximum input length
    truncation=True  #Cut the input to the desired length
  )
  completion = model.generate(
    **inputs,
    do_sample=False,  #Whether to use sampling
    max_new_tokens=GenerationLength,  #Maximum length of generation
    min_length=1,  #Minimun generation length
    exponential_decay_length_penalty=(0, -1.0101986),
    #Exponential penalty to the length that is used with beam-based generation. It is applied as an exponent to the sequence length, which in turn is used to divide the score of the sequence. Since the score is the log likelihood of the sequence (i.e. negative), length_penalty >0.0 promotes longer sequences, while length_penalty < 0.0 encourages shorter sequences.
    repetition_penalty=
    0.999,  #1 means no penalty for repitition. Less than 1 makes it just copy your code over and over.
    diversity_penalty=
    0,  # This value is subtracted from a beam’s score if it generates a token same as any beam from other group at a particular time.
    temperature=
    0.2,  #Increase to improve diversity of outputs, may cause artifacts. (max: 1)
    top_p=1,
    top_k=50,
    #suppress_tokens=[] #Ignored characters
  )  # https://huggingface.co/docs/transformers/v4.23.1/en/main_classes/text_generation#transformers.generation_utils.GenerationMixin.generate
  #https://discuss.huggingface.co/t/keyerror-when-training/24688
  raw = tokenizer.decode(completion[0])
  if raw.endswith('<|endoftext|>'):
    output = raw[:-len('<|endoftext|>')]
  else:
    output = raw
  return {'fullcode': output, 'raw': raw, 'time': time.time() - start}
