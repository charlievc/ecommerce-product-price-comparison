#!/usr/bin/env python
# coding: utf-8

# In[1]:


from search import Search
from accessweb import Lazada, Shopee, Ebay
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# In[2]:


item = Search()


# In[3]:


obj_sho = Shopee(item.getName())
df_sho = obj_sho.letsAutomateThis()


# In[4]:


obj_eba = Ebay(item.getName())
df_eba = obj_eba.letsAutomateThis()


# In[5]:


obj_laz = Lazada(item.getName())
df_laz = obj_laz.letsAutomateThis()


# In[6]:


df = pd.concat([df_sho,df_eba,df_laz])


# In[7]:


print('\n WEB PAGE STATISTICS FOR SEARCHED ITEM')
print(df.groupby(['webPage']).describe(),'\n')


# In[8]:


sns.set_style('darkgrid')
plot_title = 'PRICE DISTRIBUTION COMPARISON OF ' + item.getName()
sns.boxplot(data=df,x='webPage',y='itemPrice').set_title(plot_title)
plt.show()

