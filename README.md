This code replicates [the plots used in this analysis by The New York 
Times](https://www.nytimes.com/interactive/2018/01/27/technology/social-media-bots.html) 
using Python and R.

[Blog 
post](https://rinzewind.org/blog-en/2018/replicating-the-new-york-times-bot-twitter-analysis-with-r-and-python.html).

Just edit `config-sample.py` with the development credentials obtained for your 
account and rename it to `config.py`.
Use python 2.7
Then:
1. Install python-twitter if needed, `pip install python-twitter`
2. Run `python get_data.py account_name` to get data for that account.
3. Run `Rscript plot_data.R account_name` to save a JPG file with the desired 
   plot. Alternatively, you can start R in interactive mode and call the 
   `save_username_plot` function to obtain a ggplot2 object.
