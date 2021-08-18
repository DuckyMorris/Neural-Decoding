import matplotlib.pyplot as plt

def find_index(dict, label):
    '''
    function that finds the index of a particular label in a dictionary
    '''
    index = 0
    for key in dict:
        if key == label:
            return index
        else:
            index = index+1

    return -1

def update_plot1(fig,ax,cors,a,r,mse,cos):
    for x in range (len(a)):
        ax.clear()
        correlations = cors[x]
        label = a[x]
        r_prediction = r[x]
        mse_prediction = mse[x]
        cos_prediction = cos[x]
        if (label != 'pass'):
            #print("label: " + label + "\tr^2: " +r_prediction + "\tmse: " +mse_prediction + "\tcos: " +cos_prediction)
            keys = correlations.keys()
            values = correlations.values()
            #if count == 0:
            rects = ax.bar(keys, values)
            ax.set_ylim([0,1])
            ax.title.set_text('Bar plot showing the correlation of the current data with each class')
            ax.set_ylabel('Correlation')
                    
            for rect,h in zip(rects,values):
                rect.set_height(h)
                
            if label == r_prediction:
                rects[find_index(correlations, label)].set_color('g')
                c1 = 'g'
                c2 = 'g'
            else:
                rects[find_index(correlations, r_prediction)].set_color('r')
                rects[find_index(correlations, label)].set_color('m')
                c1 = 'r'
                c2 = 'm'
                    
            fig.canvas.draw()
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            ax.text(0.05, 0.95, "Actual: "+label, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
            ax.text(-0.7,0.93, u'\u25CF', color = c2)

            ax.text(0.05, 0.85, "Predicted: "+r_prediction, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
            ax.text(-0.7,0.83, u'\u25CF', color = c1)
            plt.pause(0.0001)

        
        else:
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            ax.text(0.05, 0.95, "Low correlation", transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)


def update_plot2(fig ,num_channels, ax, x, y, lines, count, set):
    sampled_data = set.sampled_data
    label = set.labels[0][0]['type']
    #print(len(x),len(y[0]))
    x.append(count/5)
    for i in range(num_channels):
        y[i].append(sampled_data[i][0])
        if len(x)>100:
            y[i] = y[i][1:]
    if (len(x)>100):
        x = x[1:]

    if lines == None:
        ax.title.set_text('Graph showing the average average spike firing rate')
        lines = {}
        ax.set_ylim([-1,150])
        # ax.set_yticks(range(-1, 151))
        # ax.yaxis.set_tick_params(labelsize=5)
        for i in range (num_channels):
            lines[i], = ax.plot([0], [i])

        ax.set_xlabel("Time in the experiment in seconds")
        ax.set_ylabel("Channel/Neuron number and Average Firing Rate \n spike firing rate = (y - neuron number)/(8 * 0.2) Hz")

    for i in range(num_channels):
        lines[i].set_xdata(x)
        temp =  [(a + i*0.125)*8 +1 for a in y[i]] 
        lines[i].set_ydata(temp)

    if len(x) == 100:
        ax.set_xlim([min(x),max(x)])
    else:
        ax.set_xlim([0,20])

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    for txt in ax.texts:
        txt.set_visible(False)
    ax.text(0.6, 0.95, "Image being shown: "+label, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
    fig.canvas.draw()
    fig.canvas.flush_events()

    return lines,x,y
#     # updating data values

