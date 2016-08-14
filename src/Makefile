MODULES = Authorize DeleteProduct GetProduct ListProducts UpdateProduct

package:
	for module in $(MODULES); do \
		zip -r ../$$module.zip $$module.py holmosapien; \
	done

clean:
	for module in $(MODULES); do \
		rm -f ../$$module.zip; \
	done
