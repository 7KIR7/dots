#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

[[ -f ~/.welcome_screen ]] && . ~/.welcome_screen

PS1='[\u@\h \W]\$ '
alias ls='ls --color=auto'
alias ll='ls -lav --ignore=..'   # show long listing of all except ".."
alias l='ls -lav --ignore=.?*'   # show long listing but no hidden dotfiles except "."
alias topdf='libreoffice --convert-to pdf *.doc' #convert to pdf
alias mergepdf='pdfunite *.pdf out.pdf' #merge pdfs
alias dotscopy='cd ~/.config/; cp -r {dunst,fish,kitty,mpd,ncmpcpp,neofetch,sway,swaylock,waybar,wofi} ~/Desktop/dots/; cd; cp -r .bashrc ~/Desktop/dots'
alias nhnb='nohup netbeans &'

[[ -z "$FUNCNEST" ]] && export FUNCNEST=100          # limits recursive functions, see 'man bash'

export JDTLS_HOME="$HOME/.local/share/eclipse/jdtls"
export _JAVA_AWT_WM_NONREPARENTING=1
export _JAVA_OPTIONS="-Dawt.useSystemAAFontSettings=on"

## Use the up and down arrow keys for finding a command in history
## (you can write some initial letters of the command first).
bind '"\e[A":history-search-backward'
bind '"\e[B":history-search-forward'