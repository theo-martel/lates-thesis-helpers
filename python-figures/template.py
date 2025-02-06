try:
    #Check if we are running from a pythonfigure context or not
    backend = matplotlib.get_backend()
except:
    #If matplotlib is not imported, we aren ot for sure in a pythonfigure context
    backend = ''

if backend != 'pgf' :
    #If we are not in a pythonfigure context, setup the basic imports
    import matplotlib.pyplot as plt
    figure = plt.figure()
    plt.rcdefaults()

# Write your code here



# End code

plt.tight_layout(pad=0.1)