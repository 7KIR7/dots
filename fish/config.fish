source ~/.aliases
if status is-interactive
    # Commands to run in interactive sessions can go here
	begin
	    set --local AUTOJUMP_PATH $HOME/.autojump/share/autojump/autojump.fish
	    if test -e $AUTOJUMP_PATH
	        source $AUTOJUMP_PATH
	    end
	end
end
