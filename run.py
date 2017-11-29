import os
import subprocess as sub

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--dir', '-d')
    parser.add_argument('--out', '-o', default='Out')
    args = parser.parse_args()
    
    # input file structures:
    # /
    #   (dir)/
    #       John_Lennon/
    #       Darth_Vader/
    #                   src/
    
    # output:
    # /
    #   (out)/
    #       John_Lennon/
    #       Darth_Vader/
    #                   log
    #                   output/
    #                           classificationxxxx.txt
    #                           xxxxx.bmp
    #                           xxxxx.bmp
    #                           xxxxx.bmp
    
    base_dir = args.dir # The dir that includes all the dirs with Student name as dir name
    temp_dir = 'Judge' # get other files(mnist, etc) in this dir
    out_dir = args.out
    os.system('mkdir %s'%out_dir)
    d_list = os.listdir('%s'%base_dir)
    # print d_list
    
    for d in d_list:
        output_dir = os.path.join(out_dir, d)
        os.system('mkdir %s'%output_dir)
        w_dir = os.path.join(os.getcwd(), temp_dir, 'src')
        print w_dir
        with open('%s/log'%output_dir, 'a') as out_file:
            try:
                sub_dir = os.path.join(base_dir, d, 'src')
                print sub_dir
                
                # Copy
                p1 = sub.Popen(['cp', '-r', sub_dir, '%s/'%temp_dir], stderr=sub.PIPE, stdout=sub.PIPE)
                output, errors = p1.communicate()
                if output or errors:
                    out_file.write(output)
                    out_file.write(errors)
                
                # Clean
                p2 = sub.Popen(['make', 'clean'], cwd=w_dir, stderr=sub.PIPE, stdout=sub.PIPE)
                output, errors = p2.communicate()
                if output or errors:
                    out_file.write(output)
                    out_file.write(errors)
                
                # Make
                p3 = sub.Popen(['make'], cwd=w_dir, stderr=sub.PIPE, stdout=sub.PIPE)
                output, errors = p3.communicate()
                if output or errors:
                    out_file.write(output)
                    out_file.write(errors)
                    
                # Run
                
                p4 = sub.Popen(['./proj3'], cwd=w_dir, stderr=sub.PIPE, stdout=sub.PIPE)
                output, errors = p4.communicate()
                if output or errors:
                    out_file.write(output)
                    out_file.write(errors)
                
                # Save
                output_sub = os.path.join( temp_dir, 'output')
                p4 = sub.Popen(['cp', '-r', output_sub, '%s/'%output_dir], stderr=sub.PIPE, stdout=sub.PIPE)
                output_sub = os.path.join( temp_dir, 'src', 'classification-summary.txt')
                p4 = sub.Popen(['cp', '-r', output_sub, '%s/'%output_dir], stderr=sub.PIPE, stdout=sub.PIPE)
                output_sub = os.path.join( temp_dir, 'src', 'network.txt')
                p4 = sub.Popen(['cp', '-r', output_sub, '%s/'%output_dir], stderr=sub.PIPE, stdout=sub.PIPE)
                output, errors = p4.communicate()
                if output or errors:
                    out_file.write(output)
                    out_file.write(errors)
                
                # Accuracy
                
                    
                
            except Exception as inst:
                out_file.write(str(type(inst)))
                out_file.write(str(inst))
            finally:
                os.system('du -hs %s/src'%temp_dir)
                os.system('rm -rf %s/src'%temp_dir)
                os.system('rm -rf %s/output/*'%temp_dir)