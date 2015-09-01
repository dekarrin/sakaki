################################################################################
# Sample Sakaki Control Scheme                                                 #
#                                                                              #
# This format is used to configure which key sequences map to which outputs    #
# for a particular scheme.                                                     #
#                                                                              #
# Lines consisting only of whitespace and lines whose first non-whitespace     #
# character is '#' are ignored.                                                #
#                                                                              #
# Lines consist of a right hand side and a left hand side, separated by an     #
# arrow (->). While in an app that uses a particular control scheme, typing    #
# in a key sequence that has a production will result in the sequence on the   #
# right hand side of the production to be sent to the app instead of the       #
# sequence that was typed in.                                                  #
#                                                                              #
# Sakaki only supports a single key + mod keys for the left hand side of a     #
# production; however, there may be several key sequences on the right hand    #
# side, separated by commas. These will be executed in the order that they     #
# appear.                                                                      #
#                                                                              #
# Names are the same as key and key modifier constant names in pygame:         #
# http://www.pygame.org/docs/ref/key.html                                      #
################################################################################

# first, the name attribute. This is required for all control schemes, as this
# is how they are identified
name = "example"

# A simple example; when 'A' is entered, 'B' should be sent to the app instead:
K_a -> K_s

# This example uses modifier keys; when SHIFT-'A' is pressed, ALT-'B' should be
# sent to the app:
KMOD_SHIFT K_a -> K_b KMOD_ALT

# In the above example, note that the order of mod keys with respect to 'normal'
# keys does not matter; however, consistency will make it easier to read.
# The following is exactly equivalent to the above:
KMOD_SHIFT K_a -> KMOD_ALT K_b

# This is an example of multiple targets of a production; when 'A' is pressed,
# ALT-'B' is sent to the app, followed by 'C':
K_a -> KMOD_ALT K_b, K_c
