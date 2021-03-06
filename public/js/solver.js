var start;
var logNode;
var log;

var glpStatus = new Array();
glpStatus[GLP_OPT]    = "Solution is optimal.";
glpStatus[GLP_FEAS]   = "Solution is feasible.";
glpStatus[GLP_INFEAS] = "Solution is infeasible.";
glpStatus[GLP_NOFEAS] = "Problem has no feasible solution.";
glpStatus[GLP_UNBND]  = "Problem has unbounded solution.";
glpStatus[GLP_UNDEF]  = "Solution is undefined.";

var glpRowStatus = new Array();
glpRowStatus[GLP_BS] = 'Basic';
glpRowStatus[GLP_NL] = 'LoBnd';
glpRowStatus[GLP_NU] = 'UpBnd';
glpRowStatus[GLP_NF] = 'Free';
glpRowStatus[GLP_NS] = 'Fixed';

window.initSolver = function() {
    logNode = document.getElementById("log");

    log = glp_print_func = function(value) {
        var now = new Date();
        var d = (now.getTime() - start.getTime()) / 1000;
        logNode.appendChild(document.createTextNode(value + "\n"));
        if (d > 180) throw new Error("timeout");
    };
}

function isMIP(lp) {
    return glp_get_num_int(lp) > 0;
}

function logOutput(value, filename) {
    log(value);
}

function tablecb(arg, mode, data) {
    log(data);
}

window.solveAMPL = function () {
    start = new Date(); 
    logNode.innerText = "";
    
    showPleaseWait();

    // hack to guarantee that the modal opens before starting solving the linear progran
    setTimeout(function() {
        try {

            var lp = glp_create_prob();
            var tran = glp_mpl_alloc_wksp();
            
            glp_mpl_read_model_from_string(tran, 'AMPL Model', getValueAMPLEditor());
            
            log('\nGenerating ...');
            glp_mpl_generate(tran,null,logOutput,tablecb);
            
            log('\nBuilding ...');
            glp_mpl_build_prob(tran,lp);
            
            log('\nSolving ...');
            

            var smcp = new SMCP({presolve: GLP_ON});
            glp_simplex(lp, smcp);
            
            if (isMIP(lp)) {
                log('\nInteger optimization ...')
                glp_intopt(lp);
            }
            
            hidePleaseWait();

            log('\nPost-Processing ...');
            if(lp) {
                if (glp_get_status(lp)==GLP_OPT) {
                    if (!isMIP(lp) && (glp_get_num_int(lp) > 0)) {
                       log('Linear relaxation of an MIP.');
                    } else {
                       log(glpStatus[glp_get_status(lp)]);
                    }
                } else {
                    log(glpStatus[glp_get_status(lp)]);
                }
                glp_mpl_postsolve(tran,lp,isMIP(lp)?GLP_MIP:GLP_SOL);

                log((glp_get_obj_dir(lp)==GLP_MIN?'Minimum ':'Maximum ') + glp_get_obj_name(lp) + ": " + (isMIP(lp)?glp_mip_obj_val(lp):glp_get_obj_val(lp)));

                log("\nVariables:");
                for(var i = 1; i <= glp_get_num_cols(lp); i++){
                    log(glp_get_col_name(lp, i)  + " = " + (isMIP(lp)?glp_mip_col_val(lp, i): glp_get_col_prim(lp, i)));
                }
                
                log("\nConstraints:");
                for (var i = 1; i <= glp_get_num_rows(lp); i++) {
                    if (glp_get_row_stat(lp,i) == GLP_BS) {
                        soln = isMIP(lp)? glp_mip_row_val(lp,i):glp_get_row_prim(lp,i);
                        log(glp_get_row_name(lp,i) + ": " + soln);
                    }
                }
                            
            } else {
                throw new AMPLError((isMIP()?'MILP':'LP') + " failed.");
            }
        } catch (err) {
            hidePleaseWait();

            log(err.message);
            setCursorAMPLEditor(err.line);
            return null;
        }

    }, 0);
        
    
    log('\nElapsed time: ' + (Date.now()-start)/1000 + ' seconds');
    return null;
}
