# CLI Hub bash completion script
# Source this file or add it to your bash completion directory

_hub_completion() {
    local cur prev opts scripts processes
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    # Available commands
    opts="add remove list run ps stop logs cleanup status exec"
    
    case "${prev}" in
        hub)
            COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
            return 0
            ;;
        run|remove|stop)
            if command -v hub >/dev/null 2>&1; then
                scripts=$(hub list 2>/dev/null | tail -n +4 | head -n -1 | awk '{print $1}')
                COMPREPLY=($(compgen -W "${scripts}" -- ${cur}))
            fi
            return 0
            ;;
        logs)
            if command -v hub >/dev/null 2>&1; then
                processes=$(hub ps 2>/dev/null | tail -n +4 | head -n -1 | awk '{print $1}')
                COMPREPLY=($(compgen -W "${processes}" -- ${cur}))
            fi
            return 0
            ;;
    esac
    
    # Handle flags
    case "${cur}" in
        --*)
            case "${COMP_WORDS[1]}" in
                add)
                    COMPREPLY=($(compgen -W "--description --workdir" -- ${cur}))
                    ;;
                run)
                    COMPREPLY=($(compgen -W "--background" -- ${cur}))
                    ;;
                logs)
                    COMPREPLY=($(compgen -W "--lines" -- ${cur}))
                    ;;
                exec)
                    COMPREPLY=($(compgen -W "--background --name" -- ${cur}))
                    ;;
            esac
            ;;
    esac
}

complete -F _hub_completion hub
