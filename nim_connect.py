
import configparser
import variables

from openai import OpenAI

config = configparser.ConfigParser()
config.read(variables.config_path)
api_key = config['NVIDIA']['api_key']

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = api_key
)
full_dialog = {}

def get_talk(quest:str, **kwargs):
  user = kwargs['user']
  if not full_dialog.get(user):
    full_dialog[user] = []
  print("question:", quest)
  full_dialog[user].append({"role": "user", "content": quest})
  dialog = full_dialog[user].copy()
  dialog = dialog[-10:]
  completion = client.chat.completions.create(
    model="nvidia/llama-3.1-nemotron-70b-instruct",
    # messages=[{"role":"user","content":quest}],
    messages=dialog,
    temperature=0.5,
    top_p=1,
    max_tokens=1024,
    stream=True
  )
  full_dialog[user].append({"role": "assistant", "content": ""})

  for chunk in completion:
    if chunk.choices[0].delta.content is not None:
      # print(chunk.choices[0].delta.content, end="")
      full_dialog[user][-1]['content'] += chunk.choices[0].delta.content
  print('answer:', full_dialog[user][-1]['content'])
  return full_dialog[user][-1]

if __name__ == '__main__':
  while True:
    question = input()
    gt = get_talk(question)