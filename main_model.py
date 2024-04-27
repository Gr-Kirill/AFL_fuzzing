import torch
from torch import nn
import numpy as np
from tqdm.notebook import tqdm

#Преобразование строк из файлов в массив int'ов
def create_hard_list():
    in_words = open('./model/input.json').read().split('\n')
    res_words = open('./model/result.json').read().split('\n')

    def transform(arr):
        ans = list()
        for i in arr:
            b = list()
            for j in i:
                b.append(float(ord(j)))
            ans.append(torch.tensor(b))
        return ans
    
    in_words = transform(in_words) #Преобразовали массив строк в массив ord(c)
    res_words = transform(res_words)

    return [list(item) for item in zip(in_words, res_words)] #Массив из 2 массивов int'a



class Model(nn.Module):
    def __init__(self):

        super(Model, self).__init__()

        self.lin1 = nn.Linear(30, 128)
        self.relu1 = nn.ReLU()
        self.lin2 = nn.Linear(128, 128)
        self.relu2 = nn.ReLU()
        self.lin3 = nn.Linear(128, 30)

    def forward(self, x):
        x = self.lin1(x)
        x = self.relu1(x)
        x = self.lin2(x)
        x = self.relu2(x)
        x = self.lin3(x)

        return x
    

#Выбираем что нагружаем
device = torch.device("cuda" if torch.cuda.is_available() else "cpu") #Если на NVIDIA + CUDA

model = Model() #Создание модели(инициализация) 

#
# model_path='model.pth'
# model = torch.load(model_path, map_location=device).to(device).eval()

model.to(device) #Передаем параметр на что нагружать будем

# Функция потерь
criterion = nn.MSELoss().to(device)
# Для оптимизации обучения моели
optimizer = torch.optim.Adam(model.parameters())

# print(model)  Количество параметров = количеству связей между нейронами
print("Number of parameters:", sum([p.numel() for p in model.parameters()]))

hard_list = create_hard_list() #В hard_list массив масивов intов
hard_list = hard_list[:-1] #так как последний элемент [][]

def train_model(model, epochs):

    for epoch in range(1, epochs+1):
        print(f"Epoch {epoch}/{epochs}:", flush=True)
        # Recalculate train loss on every sample using a moving average
        moving_avg_loss = 0.0
        train_losses = []
        
        #Это цикл обучения
        with tqdm() as batch_bar:
            for i, data in enumerate(hard_list):
                inputs, gt_outputs = data[0], data[1]

                inputs = inputs.to(device)
                gt_outputs = list(map(lambda x: x.to(device), gt_outputs))
                
                # Закидываем входные данные в модель
                outputs = model(inputs)
                
                # Считаем функцию потерь
                loss = 0
                for ijk in range(len(outputs)):
                    loss += criterion(outputs[ijk], gt_outputs[ijk])
                
                #Работа оптимизатора ??!
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                
                # Calculate moving average loss
                moving_avg_loss = loss.item() if i == 0 else (0.99 * moving_avg_loss + 0.01 * loss.item())
                
                # Save train batch loss
                train_losses.append(loss.item())  # Закидываю в массив значение потери
                
                #Вывод в tqdm функции потерь
                batch_bar.set_postfix_str(f"\tloss = {moving_avg_loss :.8f}")
                batch_bar.update()
                
        #Для изображения    
        print(f"Train loss: {np.mean(train_losses)}\n", flush=True)

        # Начало обучения модели
        model.train()

    print("Finished training!")


train_model(model=model, epochs=200)
torch.save(model, 'model.pth')

def test_model(str_string):
    with torch.no_grad():
        # Add batch dimension and wrap it into a tensor on the GPU
        # string = "abcdef"
        model_input = list()

        for i in str_string:
            model_input.append(float(ord(i)))

        # tensor = torch.tensor(new_string)
        model_input = torch.tensor(model_input, device=device)
        # Predict 
        new_string = model(model_input)

        list_tensor = new_string.int().tolist()
        # Преобразуем список в строку
        string_tensor = ''.join([chr(item) for item in list_tensor])

        

        #new_string = new_string.cpu().numpy()[0]

        return string_tensor

# Проверка
# string_s = '#Home:"ewqr"//,das:qwer: {"s"}'
# model_outputs = test_model(string_s)
# print(model_outputs)


